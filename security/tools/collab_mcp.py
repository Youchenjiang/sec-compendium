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
* Errors are raised as ``ValueError`` so ``collab_bus.main`` renders them as the
  usual ``ERROR ...`` line and exits 2.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import collab_protocol as protocol

REGISTRY_PATH = protocol.REPO_ROOT / ".agent" / "mcp" / "registry.json"
PROBE_PATH = protocol.REPO_ROOT / ".agent" / "mcp" / "tools" / "mcp_probe.py"

#: How long a live MCP session may run before we treat it as hung.
SESSION_TIMEOUT_SECONDS = 300


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


def _child_env(runner: dict) -> dict:
    env = dict(os.environ)
    env["PATH"] = runner["path_prepend"] + os.pathsep + env.get("PATH", "")
    env.update(runner["env"])
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
) -> dict:
    """Run one live MCP session against a registered server and return sections."""
    if not PROBE_PATH.exists():
        raise ValueError(f"MCP probe missing: {protocol.relative_posix(PROBE_PATH)}")

    entry = get_server(registry, server)
    runner = resolve_runner(entry)

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
            env=_child_env(runner),
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
        print(
            f"{name} status={entry.get('status', 'unknown')} "
            f"requires_python={python_req} runtime={runtime} "
            f"venv={venv_rel or '-'} docs={entry.get('docs', '-')}"
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
    """Live: call one tool on a registered server and print its real result."""
    arguments: dict = {}
    if args.args:
        try:
            arguments = json.loads(args.args)
        except json.JSONDecodeError as exc:
            raise ValueError(f"--args must be a JSON object: {exc}") from exc
        if not isinstance(arguments, dict):
            raise ValueError("--args must decode to a JSON object")

    registry = load_registry()
    sections = run_session(registry, args.server, call=args.tool, arguments=arguments)
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
    call.set_defaults(func=command_call)


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
