#!/usr/bin/env python3
"""MCP bridge for the governed collaboration bus.

Lets collab sessions drive registered MCP servers as ordinary CLI calls from the
collaboration execution path. The registry at ``.agent/mcp/registry.json`` is the
single source of truth; this module turns a registry entry into a runnable stdio
session and proxies ``tools/list`` / ``tools/call`` through
``.agent/mcp/tools/mcp_probe.py``.

Design notes
------------
* This module deliberately does NOT ``import mcp``: the host interpreter has no
  MCP SDK, and each server owns a venv that does. The session therefore runs in
  the *server's* venv python, which is also the interpreter that can import the
  installed server package.
* Every tool call passes the Authorization Gate first: servers that declare a
  gated capability (``command_exec``/``write``, or no capability at all) need an
  explicit allowlist entry in ``registry.authorization``, and the call is
  refused (exit 2) otherwise. Decisions are appended to an audit log.
* Secret values never reach this module from the registry: the registry records
  variable *names*, and only those names are read out of ``secrets.env`` for the
  server that declares them.
* Errors are raised as ``ValueError`` so ``collab_bus.main`` renders them as the
  usual ``ERROR ...`` line and exits 2.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import collab_protocol as protocol

REGISTRY_PATH = protocol.REPO_ROOT / ".agent" / "mcp" / "registry.json"
PROBE_PATH = protocol.REPO_ROOT / ".agent" / "mcp" / "tools" / "mcp_probe.py"
SECRETS_PATH = protocol.REPO_ROOT / "secrets.env"
GATE_LOG_PATH = protocol.RUNTIME_DIR / "mcp-gate.jsonl"

#: How long a live MCP session may run before we treat it as hung.
SESSION_TIMEOUT_SECONDS = 300

#: Capabilities that require an explicit allowlist entry before any call.
DEFAULT_GATED_CAPABILITIES = ("command_exec", "write")


def load_registry() -> dict:
    """Read the MCP registry, raising ValueError on a broken registry."""
    if not REGISTRY_PATH.exists():
        raise ValueError(f"MCP registry not found: {protocol.relative_posix(REGISTRY_PATH)}")
    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"MCP registry is not valid JSON: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("servers"), list):
        raise ValueError("MCP registry must contain a 'servers' list")
    return data


def get_server(registry: dict, name: str) -> dict:
    """Look up one registered server by name."""
    for entry in registry.get("servers", []):
        if entry.get("name") == name:
            return entry
    known = ", ".join(sorted(e.get("name", "?") for e in registry.get("servers", []))) or "(none)"
    raise ValueError(f"unknown MCP server {name!r}; registered: {known}")


# --------------------------------------------------------------------------------
# Secret plumbing (names from the registry, values only from secrets.env)
# --------------------------------------------------------------------------------


def parse_secrets_env(text: str) -> dict[str, str]:
    """Parse a ``KEY=value`` secrets file into a mapping.

    Tolerates blank lines, ``#`` comments and an optional ``export`` prefix;
    surrounding single/double quotes are stripped. Values stay literal (no
    variable expansion), so a token containing ``$`` survives unchanged.
    """
    secrets: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            continue
        secrets[key] = value
    return secrets


def declared_secret_names(entry: dict) -> list[str]:
    """Environment variable names a server is allowed to receive.

    ``secrets_binding.env`` is authoritative; the legacy ``secrets.env`` block is
    only consulted when no binding exists, so a stale note in the old field can
    never widen what a server receives. Only names are ever stored here.
    """
    names: set[str] = set()
    for block_key in ("secrets_binding", "secrets"):
        block = entry.get(block_key)
        if not isinstance(block, dict):
            continue
        for name in block.get("env") or []:
            if isinstance(name, str) and name.strip():
                names.add(name.strip())
        break
    return sorted(name for name in names if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name))


def resolve_secret_env(
    entry: dict,
    *,
    secrets_file: Path | None = None,
    process_env: dict[str, str] | None = None,
) -> tuple[dict[str, str], list[str]]:
    """Return ``(values, missing_names)`` for one server's declared names.

    Precedence: ``secrets.env`` first, then an already-set process environment
    variable of the same name. Undeclared keys in ``secrets.env`` are never
    returned, so a server cannot harvest another server's credentials.
    """
    path = Path(secrets_file) if secrets_file is not None else SECRETS_PATH
    stored: dict[str, str] = {}
    if path.exists():
        try:
            stored = parse_secrets_env(path.read_text(encoding="utf-8"))
        except OSError:
            stored = {}

    env = os.environ if process_env is None else process_env
    values: dict[str, str] = {}
    missing: list[str] = []
    for name in declared_secret_names(entry):
        if name in stored:
            values[name] = stored[name]
        elif env.get(name):
            values[name] = env[name]
        else:
            missing.append(name)
    return values, missing


def secrets_binding(entry: dict) -> dict:
    """Normalise a server's secret contract (``required``/``inject``/names)."""
    block = entry.get("secrets_binding")
    if not isinstance(block, dict):
        block = entry.get("secrets") if isinstance(entry.get("secrets"), dict) else {}
    return {
        "required": bool(block.get("required")),
        "inject": block.get("inject") or ("host-env" if declared_secret_names(entry) else "none"),
        "env": declared_secret_names(entry),
    }


# --------------------------------------------------------------------------------
# Authorization Gate (capability classes + command-exec allowlist)
# --------------------------------------------------------------------------------


def capability_classes(entry: dict) -> list[str]:
    """Declared capability classes, or ``['unclassified']`` when absent.

    An entry that declares nothing is treated as gated: absence of evidence is
    not evidence of harmlessness.
    """
    declared = entry.get("capability_class")
    if isinstance(declared, str):
        declared = [declared]
    if not isinstance(declared, list):
        return ["unclassified"]
    classes = sorted({str(item).strip().lower() for item in declared if str(item).strip()})
    return classes or ["unclassified"]


def authorization_policy(registry: dict) -> dict:
    """Normalise ``registry.authorization`` into a predictable policy dict."""
    policy = registry.get("authorization")
    if not isinstance(policy, dict):
        policy = {}
    gated = policy.get("applies_to_capabilities") or list(DEFAULT_GATED_CAPABILITIES)
    return {
        "policy_version": policy.get("policy_version", 0),
        "default_decision": policy.get("default_decision", "deny"),
        "applies_to_capabilities": sorted({str(item).lower() for item in gated}),
        "authorization_env": policy.get("authorization_env") or "MCP_AUTHORIZATION",
        "command_exec_allowlist": list(policy.get("command_exec_allowlist") or []),
    }


def _iter_strings(value: object):
    """Yield every string inside arbitrarily nested call arguments."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _iter_strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _iter_strings(item)


def _looks_like_path(value: str) -> bool:
    return os.path.isabs(value) or "/" in value or "\\" in value


def _within_roots(value: str, roots: list[str]) -> bool:
    """Whether a path-like argument resolves inside one of the allowed roots."""
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = protocol.REPO_ROOT / candidate
    try:
        resolved = candidate.resolve()
    except OSError:
        return False
    for root in roots:
        base = Path(str(root))
        if not base.is_absolute():
            base = protocol.REPO_ROOT / base
        try:
            base_resolved = base.resolve()
        except OSError:
            continue
        if resolved == base_resolved or base_resolved in resolved.parents:
            return True
    return False


def _allowlist_entry(policy: dict, server: str) -> dict | None:
    for entry in policy.get("command_exec_allowlist") or []:
        if isinstance(entry, dict) and entry.get("server") == server:
            return entry
    return None


def gate_decision(
    registry: dict,
    server: str,
    tool: str | None,
    arguments: dict | None = None,
    *,
    authorized_reason: str = "",
    process_env: dict[str, str] | None = None,
) -> dict:
    """Decide whether a tool call is authorized, without running anything.

    Returns ``{'decision': 'allow'|'deny', 'reason': str, ...}``. Unknown or
    retired servers raise ``ValueError`` (handled by the caller as exit 2).
    """
    policy = authorization_policy(registry)
    entry = get_server(registry, server)
    capabilities = capability_classes(entry)
    gated = sorted(set(capabilities) & set(policy["applies_to_capabilities"]))
    decision: dict = {
        "server": server,
        "tool": tool,
        "capabilities": capabilities,
        "gated_capabilities": gated,
        "decision": "allow",
        "reason": "",
    }
    if not gated:
        decision["reason"] = "server declares no gated capability"
        return decision

    match = _allowlist_entry(policy, server)
    if match is None:
        decision["decision"] = "deny"
        decision["reason"] = (
            f"{server} declares {', '.join(gated)} but has no entry in "
            "registry.authorization.command_exec_allowlist; default decision is deny"
        )
        return decision

    decision["allowlist"] = {
        key: match.get(key)
        for key in ("tools", "paths_allow", "deny_patterns", "requires_authorization", "expires", "note")
        if key in match
    }

    allowed_tools = [str(item) for item in match.get("tools") or []]
    if tool and tool not in allowed_tools and "*" not in allowed_tools:
        decision["decision"] = "deny"
        decision["reason"] = (
            f"tool {tool!r} is not allowlisted for {server} "
            f"(allowed: {', '.join(allowed_tools) or 'none'})"
        )
        return decision

    expires = match.get("expires")
    if expires:
        try:
            expired = date.fromisoformat(str(expires)) < date.today()
        except ValueError:
            expired = True
        if expired:
            decision["decision"] = "deny"
            decision["reason"] = f"allowlist entry for {server} expired on {expires}"
            return decision

    values = list(_iter_strings(arguments or {}))
    for pattern in match.get("deny_patterns") or []:
        try:
            matcher = re.compile(str(pattern))
        except re.error:
            continue
        for value in values:
            if matcher.search(value):
                decision["decision"] = "deny"
                decision["reason"] = (
                    f"argument matches deny pattern {pattern!r}: "
                    f"{value[:120]!r}"
                )
                return decision

    roots = [str(root) for root in match.get("paths_allow") or []]
    for value in values:
        if _looks_like_path(value) and not _within_roots(value, roots):
            decision["decision"] = "deny"
            decision["reason"] = (
                f"path argument outside the allowlisted scope for {server}: {value[:160]!r} "
                f"(allowed roots: {', '.join(roots) or 'none declared'})"
            )
            return decision

    if match.get("requires_authorization", True):
        env_name = match.get("authorization_env") or policy["authorization_env"]
        env = os.environ if process_env is None else process_env
        if not str(authorized_reason or "").strip():
            decision["decision"] = "deny"
            decision["reason"] = (
                f"{server} is command-capable: pass --authorized \"<why this call is "
                f"authorized>\" so the approval is recorded in the audit log"
            )
            return decision
        if not env.get(env_name):
            decision["decision"] = "deny"
            decision["reason"] = (
                f"{server} is command-capable and requires {env_name} to be set "
                "(put the value in secrets.env; the registry only records the name)"
            )
            return decision

    decision["reason"] = "allowlisted"
    return decision


def record_gate_decision(decision: dict, *, reason: str = "", mode: str = "enforce",
                         log_path: Path | None = None) -> None:
    """Append one audit line; a logging failure never blocks or unwinds a call."""
    path = Path(log_path) if log_path is not None else GATE_LOG_PATH
    record = {
        "at": protocol.utc_timestamp(),
        "mode": mode,
        "server": decision.get("server"),
        "tool": decision.get("tool"),
        "capabilities": decision.get("capabilities"),
        "decision": decision.get("decision"),
        "reason": decision.get("reason"),
        "authorized_reason": reason,
    }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        pass


def enforce_gate(
    registry: dict,
    server: str,
    tool: str | None,
    arguments: dict | None = None,
    *,
    authorized_reason: str = "",
    process_env: dict[str, str] | None = None,
) -> dict:
    """Apply the gate and raise ``ValueError`` when the call is not authorized."""
    decision = gate_decision(
        registry,
        server,
        tool,
        arguments,
        authorized_reason=authorized_reason,
        process_env=process_env,
    )
    record_gate_decision(decision, reason=authorized_reason)
    if decision["decision"] != "allow":
        raise ValueError(f"authorization gate denied {server}/{tool}: {decision['reason']}")
    return decision


def _venv_binary(venv: Path, name: str) -> Path | None:
    """Locate ``name`` inside a venv on either Windows (Scripts) or POSIX (bin)."""
    for sub, suffix in (("Scripts", ".exe"), ("bin", "")):
        base = venv / sub
        for candidate in (base / f"{name}{suffix}", base / name):
            if candidate.exists():
                return candidate
    return None


def resolve_runner(entry: dict) -> dict:
    """Turn a registry entry's ``runner`` block into concrete executables.

    Returns a dict with ``command`` (server executable), ``args``, ``python``
    (venv interpreter used to run the MCP client session), ``env`` (resolved
    child environment overrides) and ``path_prepend`` (so the server can find
    its own binaries, e.g. ``semgrep``).
    """
    runner = entry.get("runner")
    if not isinstance(runner, dict):
        raise ValueError(
            f"{entry.get('name', '?')}: registry entry has no 'runner' block; "
            "add the server's venv/script/args so the collab bus can spawn it"
        )

    venv_rel = runner.get("venv")
    if not venv_rel:
        raise ValueError(f"{entry.get('name', '?')}: runner.venv is required")

    venv = protocol.REPO_ROOT / venv_rel
    if not venv.exists():
        raise ValueError(
            f"{entry.get('name', '?')}: runtime not provisioned at {venv_rel} "
            f"-> follow {entry.get('docs', '.agent/mcp/servers/')} install steps"
        )

    script = runner.get("script")
    if not script:
        raise ValueError(f"{entry.get('name', '?')}: runner.script is required")

    command = _venv_binary(venv, script)
    if command is None:
        raise ValueError(
            f"{entry.get('name', '?')}: {script!r} not found under {venv_rel}; "
            "the runtime is incomplete or the install recipe was not run"
        )

    python = _venv_binary(venv, "python")
    if python is None:
        raise ValueError(f"{entry.get('name', '?')}: python interpreter missing in {venv_rel}")

    env: dict[str, str] = {}
    for key, value in (runner.get("env") or {}).items():
        path_value = protocol.REPO_ROOT / value
        env[key] = str(path_value if not Path(value).is_absolute() else Path(value))

    return {
        "command": str(command),
        "args": list(runner.get("args") or []),
        "python": str(python),
        "env": env,
        "path_prepend": str(Path(command).parent),
    }


def _child_env(runner: dict, secrets: dict[str, str] | None = None) -> dict:
    """Child environment for one session: runner overrides plus declared secrets only."""
    env = dict(os.environ)
    env["PATH"] = runner["path_prepend"] + os.pathsep + env.get("PATH", "")
    env.update(runner["env"])
    for name, value in (secrets or {}).items():
        env[name] = value
    return env


def _parse_sections(stdout: str) -> dict:
    """Split probe output into ``{section: payload}``, JSON-decoding each block."""
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in stdout.splitlines():
        if line.startswith("### "):
            current = line[4:].strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)

    decoded: dict[str, object] = {}
    for name, body in sections.items():
        text = "\n".join(body).strip()
        try:
            decoded[name] = json.loads(text) if text else None
        except json.JSONDecodeError:
            decoded[name] = text
    return decoded


def run_session(
    registry: dict,
    server: str,
    call: str | None = None,
    arguments: dict | None = None,
    *,
    authorized_reason: str = "",
) -> dict:
    """Run one live MCP session against a registered server and return sections.

    The Authorization Gate runs before anything is spawned, and the child only
    receives the secret variables the registry declares for this server.
    """
    if not PROBE_PATH.exists():
        raise ValueError(f"MCP probe missing: {protocol.relative_posix(PROBE_PATH)}")

    entry = get_server(registry, server)
    enforce_gate(registry, server, call, arguments, authorized_reason=authorized_reason)
    runner = resolve_runner(entry)

    secrets, missing = resolve_secret_env(entry)
    binding = secrets_binding(entry)
    if missing and binding["required"]:
        raise ValueError(
            f"{server}: missing required secret env names {', '.join(missing)}; "
            "add them to secrets.env (the registry records names only)"
        )

    cmd = [
        runner["python"],
        str(PROBE_PATH),
        "--cmd",
        runner["command"],
        "--path-prepend",
        runner["path_prepend"],
    ]
    for arg in runner["args"]:
        # Server argv values routinely start with "-" (e.g. ``-t``); pass them in
        # ``--arg=value`` form so argparse never mistakes them for its own flags.
        cmd.extend([f"--arg={arg}"])
    if call:
        cmd.extend(["--call", call])
        cmd.extend(["--arguments", json.dumps(arguments or {})])

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=_child_env(runner, secrets),
            cwd=str(protocol.REPO_ROOT),
            timeout=SESSION_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValueError(
            f"MCP session for {server!r} exceeded {SESSION_TIMEOUT_SECONDS}s"
        ) from exc

    sections = _parse_sections(proc.stdout or "")
    if "initialize" not in sections:
        detail = (proc.stderr or proc.stdout or "").strip()[-500:]
        raise ValueError(
            f"MCP session for {server!r} failed to initialize (exit {proc.returncode})"
            + (f": {detail}" if detail else "")
        )

    if call and "tools/call.result" not in sections:
        detail = (proc.stderr or proc.stdout or "").strip()[-500:]
        raise ValueError(
            f"MCP call {call!r} on {server!r} produced no result"
            + (f": {detail}" if detail else "")
        )
    return sections


# --------------------------------------------------------------------------------
# CLI commands
# --------------------------------------------------------------------------------


def _parse_arguments(raw: str) -> dict:
    """Decode a ``--args`` JSON object, raising ValueError on a bad payload."""
    if not raw:
        return {}
    try:
        arguments = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"--args must be a JSON object: {exc}") from exc
    if not isinstance(arguments, dict):
        raise ValueError("--args must decode to a JSON object")
    return arguments


def command_list(args: argparse.Namespace) -> int:
    """Offline: show registered servers and whether their runtime is provisioned."""
    registry = load_registry()
    servers = registry.get("servers", [])
    if not servers:
        print("No MCP servers registered.")
        return 0

    for entry in servers:
        name = entry.get("name", "?")
        runner = entry.get("runner") or {}
        venv_rel = runner.get("venv", "")
        venv = protocol.REPO_ROOT / venv_rel if venv_rel else None
        script_ok = bool(venv and _venv_binary(venv, runner.get("script", "script")))
        runtime = "ready" if script_ok else "missing"
        python_req = entry.get("runtime", {}).get("requires_python", "any")
        placement = entry.get("placement") or {}
        print(
            f"{name} status={entry.get('status', 'unknown')} "
            f"requires_python={python_req} runtime={runtime} "
            f"venv={venv_rel or '-'} holder={placement.get('holder_class', '-')} "
            f"capabilities={','.join(capability_classes(entry))} "
            f"gated={'yes' if set(capability_classes(entry)) & set(authorization_policy(registry)['applies_to_capabilities']) else 'no'} "
            f"docs={entry.get('docs', '-')}"
        )

    retired = registry.get("retired", [])
    for entry in retired:
        print(f"{entry.get('name', '?')} status=retired replaced_by={entry.get('replaced_by', '-')}")
    return 0


def command_tools(args: argparse.Namespace) -> int:
    """Live: list the tools a registered server actually exposes."""
    registry = load_registry()
    sections = run_session(registry, args.server)
    tools = (sections.get("tools/list") or {}).get("tools") or []
    info = (sections.get("initialize") or {}).get("serverInfo") or {}
    print(f"{args.server} serverInfo={info.get('name')}/{info.get('version')} tools={len(tools)}")
    for tool in tools:
        if args.verbose:
            description = " ".join(str(tool.get("description", "")).split())[:200]
            print(f"  {tool.get('name')} - {description}")
        else:
            print(f"  {tool.get('name')}")
    return 0


def command_call(args: argparse.Namespace) -> int:
    """Live: call one tool on a registered server and print its real result.

    The Authorization Gate runs first; a denied call prints ``ERROR ...`` and
    exits 2 without ever spawning the server.
    """
    arguments = _parse_arguments(args.args)
    registry = load_registry()
    sections = run_session(
        registry,
        args.server,
        call=args.tool,
        arguments=arguments,
        authorized_reason=getattr(args, "authorized", "") or "",
    )
    result = sections.get("tools/call.result") or {}

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
        return 0 if not result.get("isError") else 1

    if result.get("isError"):
        payload = result.get("content") or []
        message = payload[0].get("text") if payload and isinstance(payload[0], dict) else str(result)
        raise ValueError(f"{args.tool} failed: {message}")

    structured = result.get("structuredContent")
    if isinstance(structured, dict) and "result" in structured:
        print(structured["result"])
    else:
        payload = result.get("content") or []
        for block in payload if isinstance(payload, list) else []:
            if isinstance(block, dict) and block.get("text") is not None:
                print(block["text"])
        if not payload:
            print(json.dumps(structured, indent=2, ensure_ascii=False, default=str))
    return 0


def command_gate(args: argparse.Namespace) -> int:
    """Offline: evaluate the Authorization Gate for a call without running it."""
    arguments = _parse_arguments(args.args)
    registry = load_registry()
    try:
        decision = gate_decision(
            registry,
            args.server,
            args.tool,
            arguments,
            authorized_reason=getattr(args, "authorized", "") or "",
        )
    except ValueError as exc:
        record_gate_decision(
            {"server": args.server, "tool": args.tool, "decision": "deny", "reason": str(exc)},
            reason=getattr(args, "authorized", "") or "",
            mode="dry-run",
        )
        print(f"deny {args.server}/{args.tool}: {exc}")
        return 2

    record_gate_decision(
        decision, reason=getattr(args, "authorized", "") or "", mode="dry-run"
    )
    print(json.dumps(decision, indent=2, ensure_ascii=False, default=str))
    return 0 if decision["decision"] == "allow" else 2


def command_secrets(args: argparse.Namespace) -> int:
    """Offline: show which secret names a server may receive and their readiness.

    Values are never printed - only the declared names and whether each one
    resolves from ``secrets.env`` (or an already-set process variable).
    """
    registry = load_registry()
    entry = get_server(registry, args.server)
    binding = secrets_binding(entry)
    values, _missing = resolve_secret_env(entry)
    print(
        f"{args.server} required={binding['required']} inject={binding['inject']} "
        f"declared={len(binding['env'])}"
    )
    if not binding["env"]:
        print("  (no secret declared: the registry grants this server no variables)")
        return 0
    for name in binding["env"]:
        print(f"  {name} {'present' if name in values else 'missing'}")
    return 0


def add_subcommands(parser: argparse.ArgumentParser) -> None:
    """Attach the ``mcp`` command group to an existing parser."""
    sub = parser.add_subparsers(dest="mcp_command", required=True)

    listing = sub.add_parser("list", help="Show registered MCP servers and runtime readiness")
    listing.set_defaults(func=command_list)

    tools = sub.add_parser("tools", help="Live MCP session: list a server's tools")
    tools.add_argument("--server", required=True)
    tools.add_argument("--verbose", action="store_true", help="Include tool descriptions")
    tools.set_defaults(func=command_tools)

    call = sub.add_parser("call", help="Live MCP session: call one tool on a server")
    call.add_argument("--server", required=True)
    call.add_argument("--tool", required=True)
    call.add_argument("--args", default="", help="JSON object of tool arguments")
    call.add_argument("--json", action="store_true", help="Emit the raw result JSON")
    call.add_argument(
        "--authorized",
        default="",
        help="Reason this command-capable call is authorized; recorded in the gate audit log",
    )
    call.set_defaults(func=command_call)

    gate = sub.add_parser(
        "gate", help="Offline: evaluate the authorization gate for a call without running it"
    )
    gate.add_argument("--server", required=True)
    gate.add_argument("--tool", default=None)
    gate.add_argument("--args", default="", help="JSON object of tool arguments")
    gate.add_argument("--authorized", default="", help="Reason an approved call would record")
    gate.set_defaults(func=command_gate)

    secrets = sub.add_parser(
        "secrets", help="Offline: show a server's declared secret names and their readiness"
    )
    secrets.add_argument("--server", required=True)
    secrets.set_defaults(func=command_secrets)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="MCP bridge for the governed collaboration bus")
    add_subcommands(parser)
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ValueError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
