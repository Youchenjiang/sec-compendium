#!/usr/bin/env python3
"""Node transport planners for the governed MCP registry.

The registry says *where* a server belongs (``placement.holder_class``) and *how*
to start it (``runner``). For the host gateway that is a local stdio spawn. This
module turns every other holder into a concrete launch plan:

======================  ====================  =========================================
holder_class            transport             how a session reaches the server
======================  ====================  =========================================
``host_gateway``        ``stdio_local``       spawn the server's own venv executable
``kali``                ``ssh``               ``ssh`` into the node and run argv there
``flare_vm``            ``vmrun_guest``       VMware Guest Ops file bridge (no port)
``container``           ``container``         ``docker run --rm -i <image> <argv>``
======================  ====================  =========================================

Whatever the transport, the thing the MCP client talks to is still a stdio
process: ``ssh``, ``docker -i`` and the vmrun bridge all forward stdin/stdout, so
``.agent/mcp/tools/mcp_probe.py`` needs no transport awareness at all.

Two rules are enforced in code, not merely documented:

1. **Secret values stay on the host gateway.** ``exec.env`` may not contain a
   ``{"secret": ...}`` reference, and only ``container.secrets`` - an explicit
   list of variable names forwarded as ``docker -e NAME``, where the value is
   read from the wrapper's own environment and never appears in argv - may cross
   a node boundary. Node credentials (SSH host/user, VM guest login) are resolved
   on the host and passed to the wrapper, never to the server.
2. **No session may reach outside the repository.** Container mounts must
   resolve inside ``repo_root``, so a node can never be handed ``$HOME`` or ``/``.

A plan records the secret *names* a wrapper needs; the caller (``collab_mcp``)
resolves the values from ``secrets.env`` and injects them into the wrapper's
environment only. Values never enter the plan, so plans are safe to print.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import shutil
from pathlib import Path

#: Transports a registry entry may declare.
NODE_TRANSPORTS = ("stdio_local", "ssh", "container", "vmrun_guest")

#: Default transport per placement holder class (``policy.node_transports`` may override).
HOLDER_DEFAULT_TRANSPORT = {
    "host_gateway": "stdio_local",
    "kali": "ssh",
    "flare_vm": "vmrun_guest",
    "container": "container",
}

DEFAULT_SSH_PORT = "22"
#: ``BatchMode`` turns a missing key into a fast failure instead of a password prompt
#: that would hang a non-interactive session.
DEFAULT_SSH_OPTIONS = (
    "-o",
    "BatchMode=yes",
    "-o",
    "StrictHostKeyChecking=accept-new",
    "-o",
    "ConnectTimeout=15",
)
DEFAULT_VMRUN = r"C:\MyAPP\VMware Workstation\vmrun.exe"
GUEST_DIR_WINDOWS = r"C:\Windows\Temp\mcp-bridge"
DEFAULT_GUEST_PYTHON = "python.exe"
DEFAULT_POLL_INTERVAL = "0.4"
DEFAULT_IDLE_SECONDS = "120"
DEFAULT_COPY_TIMEOUT = "60"
DEFAULT_RESPONSE_TIMEOUT = "120"

_ENV_NAME_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


class TransportError(ValueError):
    """A node transport cannot be planned; ``collab_mcp`` renders it as ERROR/exit 2."""


def normalise_policy(registry: dict | None) -> dict:
    """Read ``registry.policy.node_transports`` into a predictable dict."""
    policy = (registry or {}).get("policy") or {}
    block = policy.get("node_transports")
    if not isinstance(block, dict):
        block = {}
    holders = dict(HOLDER_DEFAULT_TRANSPORT)
    declared = block.get("holder_defaults")
    if isinstance(declared, dict):
        for holder, transport in declared.items():
            if isinstance(transport, str) and transport.strip():
                holders[str(holder)] = transport.strip()
    return {
        "policy_version": block.get("policy_version", 0),
        "holder_defaults": holders,
        "probe_env": block.get("probe_env") or "",
        "guest_bridge": block.get("guest_bridge") or "",
        "vmrun_bridge": block.get("vmrun_bridge") or "",
    }


def node_block(entry: dict) -> dict:
    """The entry's ``runner.node`` block, or an empty dict when it has none."""
    runner = entry.get("runner")
    node = runner.get("node") if isinstance(runner, dict) else None
    return node if isinstance(node, dict) else {}


def transport_for(entry: dict, *, policy: dict | None = None) -> str:
    """Resolve which transport a registered server must be reached through.

    Precedence: ``runner.node.transport`` -> ``runtime.node_transport`` ->
    the holder default for ``placement.holder_class``. The derived value is what
    keeps the registry honest: a server placed on Kali is reached over SSH, and
    an entry can only deviate by saying so explicitly.
    """
    name = entry.get("name", "?")
    holders = (policy or normalise_policy(None))["holder_defaults"]
    node = node_block(entry)
    declared = node.get("transport") or (entry.get("runtime") or {}).get("node_transport")
    if declared:
        declared = str(declared).strip()
        if declared not in NODE_TRANSPORTS:
            raise TransportError(
                f"{name}: unknown node transport {declared!r}; known transports: "
                + ", ".join(NODE_TRANSPORTS)
            )
        return declared

    holder = (entry.get("placement") or {}).get("holder_class") or "host_gateway"
    holder = str(holder).strip()
    if holder not in holders:
        raise TransportError(
            f"{name}: unknown placement.holder_class {holder!r}; known holders: "
            + ", ".join(sorted(holders))
            + " (or set runner.node.transport explicitly)"
        )
    transport = holders[holder]
    if transport not in NODE_TRANSPORTS:
        raise TransportError(
            f"{name}: registry.policy.node_transports maps {holder!r} to unknown transport "
            f"{transport!r}"
        )
    return transport


def venv_python(venv: Path) -> Path | None:
    """Locate a venv interpreter on either Windows (Scripts) or POSIX (bin)."""
    for sub, suffix in (("Scripts", ".exe"), ("bin", "")):
        for candidate in (venv / sub / f"python{suffix}", venv / sub / "python3"):
            if candidate.exists():
                return candidate
    return None


def resolve_probe_python(entry: dict, *, repo_root: Path, policy: dict | None = None) -> Path:
    """Host-side interpreter that runs the MCP client for a node transport.

    A node transport talks stdio to a *wrapper*, so the MCP SDK must exist on the
    host gateway. Server venvs on a node cannot serve that purpose (and for a
    container they do not exist at all), hence a dedicated probe environment is
    declared once in the registry policy and may be overridden per entry.
    """
    name = entry.get("name", "?")
    policy = policy or normalise_policy(None)
    rel = node_block(entry).get("probe_env") or policy.get("probe_env")
    if not rel:
        raise TransportError(
            f"{name}: node transport needs a host-side probe interpreter; set "
            "registry.policy.node_transports.probe_env (or runner.node.probe_env)"
        )
    venv = Path(str(rel))
    if not venv.is_absolute():
        venv = repo_root / venv
    python = venv_python(venv)
    if python is None:
        raise TransportError(
            f"{name}: probe environment not provisioned at {rel}; create it with: "
            f"python -m venv {rel} && {rel}/Scripts/python -m pip install \"mcp<2\" "
            "(the wrapper talks stdio to the node, so the MCP SDK lives on the host)"
        )
    return python


def _secret_name(value: object, *, field: str, entry_name: str) -> str | None:
    """Environment variable name a field points at, or ``None`` when it is a literal."""
    if not isinstance(value, dict):
        return None
    secret = value.get("secret") or value.get("secret_env")
    if not isinstance(secret, str) or not secret.strip():
        raise TransportError(
            f"{entry_name}: {field} must be a literal or {{\"secret\": \"NAME\"}}, got {value!r}"
        )
    return secret.strip()


def _field_value(
    value: object,
    *,
    field: str,
    entry_name: str,
    secret_lookup=None,
) -> str:
    """Text for one node field.

    A ``{"secret": "NAME"}`` reference is resolved through ``secret_lookup``,
    which is how node addressing reaches the wrapper's argv (``ssh`` needs the
    host and user as arguments) while the value itself is fetched from
    ``secrets.env`` by the caller. Without a lookup - the describe/``mcp launch``
    path - the field renders as ``<NAME>`` so a plan is always printable and can
    never leak a value.
    """
    name = _secret_name(value, field=field, entry_name=entry_name)
    if name is not None:
        if secret_lookup is None:
            return f"<{name}>"
        return str(secret_lookup(name))
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise TransportError(
            f"{entry_name}: {field} must be a literal or {{\"secret\": \"NAME\"}}, got {value!r}"
        )
    text = str(value).strip()
    if not text:
        raise TransportError(f"{entry_name}: {field} must not be empty")
    return text


def _int_field(block: dict, key: str, default: str, *, entry_name: str, field: str) -> str:
    raw = block.get(key, default)
    if _secret_name(raw, field=field, entry_name=entry_name) is not None:
        raise TransportError(f"{entry_name}: {field} must be a literal, not a secret reference")
    text = _field_value(raw, field=field, entry_name=entry_name)
    try:
        number = float(text)
    except ValueError as exc:
        raise TransportError(f"{entry_name}: {field} must be numeric, got {text!r}") from exc
    if number < 0:
        raise TransportError(f"{entry_name}: {field} must not be negative")
    return text


def _exec_block(node: dict, entry_name: str) -> dict:
    """Normalise ``runner.node.exec`` (the argv that runs the server *on the node*)."""
    block = node.get("exec")
    if not isinstance(block, dict) or not block.get("command"):
        raise TransportError(
            f"{entry_name}: runner.node.exec.command is required for a node transport"
        )
    raw_env = block.get("env") or {}
    if not isinstance(raw_env, dict):
        raise TransportError(f"{entry_name}: runner.node.exec.env must be an object")
    env: dict[str, str] = {}
    for key, value in raw_env.items():
        field = f"exec.env.{key}"
        name = _secret_name(value, field=field, entry_name=entry_name)
        if name is not None:
            raise TransportError(
                f"{entry_name}: {field} references secret {name!r}; secret values must not "
                "travel to a node. Keep the variable host-side, or declare it in "
                "container.secrets to forward it explicitly with `docker -e NAME`"
            )
        env[str(key)] = _field_value(value, field=field, entry_name=entry_name)
    args = block.get("args") or []
    if not isinstance(args, list):
        raise TransportError(f"{entry_name}: runner.node.exec.args must be a list")
    return {
        "command": str(block["command"]),
        "args": [str(item) for item in args],
        "cwd": str(block["cwd"]) if block.get("cwd") else None,
        "env": env,
        "path_prepend": str(block["path_prepend"]) if block.get("path_prepend") else None,
    }


def _require_binary(name: str, *, entry_name: str, which) -> str:
    found = which(name)
    if not found:
        raise TransportError(
            f"{entry_name}: {name!r} is required for this node transport but was not found on "
            "the host gateway's PATH"
        )
    return str(found)


def _remote_script(exec_block: dict) -> str:
    """POSIX shell line that runs the server argv on a node.

    The whole line is quoted once for ``ssh`` and once for the remote shell, so
    arguments containing spaces, quotes or ``$`` survive intact.
    """
    pieces: list[str] = []
    if exec_block["cwd"]:
        pieces.append(f"cd {shlex.quote(exec_block['cwd'])}")
    env_items = [f"{key}={shlex.quote(value)}" for key, value in sorted(exec_block["env"].items())]
    if exec_block["path_prepend"]:
        env_items.insert(0, f"PATH={shlex.quote(exec_block['path_prepend'])}:$PATH")
    inner = shlex.join([exec_block["command"], *exec_block["args"]])
    if env_items:
        inner = "exec env " + " ".join(env_items) + " " + inner
    pieces.append(inner)
    return " && ".join(pieces)


def _plan_ssh(entry_name: str, node: dict, exec_block: dict, *, which, secret_lookup) -> dict:
    conf = node.get("ssh")
    if not isinstance(conf, dict):
        raise TransportError(f"{entry_name}: transport 'ssh' needs a runner.node.ssh block")
    for required in ("host", "user"):
        if not conf.get(required):
            raise TransportError(f"{entry_name}: runner.node.ssh.{required} is required")

    secret_names: list[str] = []
    addresses: dict[str, str] = {}
    for field in ("host", "user"):
        name = _secret_name(conf[field], field=f"ssh.{field}", entry_name=entry_name)
        if name:
            secret_names.append(name)
        # The address is not a secret, but it is resolved here because ssh needs it
        # on its argument list; only ``password_secret`` is kept off argv.
        addresses[field] = _field_value(
            conf[field], field=f"ssh.{field}", entry_name=entry_name, secret_lookup=secret_lookup
        )

    port = _field_value(
        conf.get("port", DEFAULT_SSH_PORT), field="ssh.port", entry_name=entry_name
    )
    options = [str(item) for item in conf.get("options") or DEFAULT_SSH_OPTIONS]

    ssh_bin = _require_binary("ssh", entry_name=entry_name, which=which)
    command = ssh_bin
    args: list[str] = []
    env: dict[str, str] = {}
    notes: list[str] = ["key-based ssh (BatchMode); no secret value is sent to the node"]

    password_secret = conf.get("password_secret")
    if password_secret:
        password_name = str(password_secret).strip()
        if not _ENV_NAME_RE.fullmatch(password_name):
            raise TransportError(
                f"{entry_name}: ssh.password_secret must be an environment variable name"
            )
        _require_binary("sshpass", entry_name=entry_name, which=which)
        command = _require_binary("sshpass", entry_name=entry_name, which=which)
        # sshpass reads the password from SSHPASS, so the value stays out of argv.
        args.extend(["-e", ssh_bin])
        secret_names.append(password_name)
        env["SSHPASS"] = _field_value(
            {"secret": password_name},
            field="ssh.password_secret",
            entry_name=entry_name,
            secret_lookup=secret_lookup,
        )
        notes.append("password auth via sshpass -e (value passed through SSHPASS)")

    args.extend(options)
    args.extend(["-p", port])
    args.append(f"{addresses['user']}@{addresses['host']}")
    args.append(f"sh -c {shlex.quote(_remote_script(exec_block))}")

    return {
        "transport": "ssh",
        "command": command,
        "args": args,
        "env": env,
        "path_prepend": str(Path(ssh_bin).parent),
        "secret_names": secret_names,
        "env_from_secrets": {},
        "forwarded_secrets": [],
        "notes": notes,
    }


def _plan_container(
    entry_name: str, node: dict, exec_block: dict, *, repo_root: Path, which, secret_lookup
) -> dict:
    conf = node.get("container")
    if not isinstance(conf, dict) or not conf.get("image"):
        raise TransportError(
            f"{entry_name}: transport 'container' needs runner.node.container.image"
        )
    docker = _require_binary("docker", entry_name=entry_name, which=which)

    args = ["run", "--rm", "-i"]
    if conf.get("name"):
        args.extend(["--name", str(conf["name"])])
    # Fail closed on networking: anything that needs the network must say so.
    network = conf.get("network") or "none"
    args.extend(["--network", str(network)])
    if conf.get("user"):
        args.extend(["--user", str(conf["user"])])

    notes: list[str] = [f"network={network}"]
    mounts = conf.get("mounts") or []
    if not isinstance(mounts, list):
        raise TransportError(f"{entry_name}: runner.node.container.mounts must be a list")
    for mount in mounts:
        if not isinstance(mount, dict) or not mount.get("host") or not mount.get("container"):
            raise TransportError(
                f"{entry_name}: each container mount needs 'host' and 'container', got {mount!r}"
            )
        host_rel = str(mount["host"])
        host_path = Path(host_rel)
        if not host_path.is_absolute():
            host_path = repo_root / host_path
        host_path = host_path.resolve()
        root = Path(repo_root).resolve()
        if host_path != root and root not in host_path.parents:
            raise TransportError(
                f"{entry_name}: refusing to mount {host_rel!r} outside the repository "
                f"({repo_root}); nodes never receive the home directory or the filesystem root"
            )
        container_path = str(mount["container"])
        if not container_path.startswith("/"):
            raise TransportError(
                f"{entry_name}: container mount target must be an absolute path, got {container_path!r}"
            )
        mode = str(mount.get("mode") or "ro")
        if mode not in ("ro", "rw"):
            raise TransportError(f"{entry_name}: container mount mode must be 'ro' or 'rw'")
        args.extend(["-v", f"{host_path}:{container_path}:{mode}"])
        notes.append(f"mount {host_rel} -> {container_path}:{mode}")

    workdir = conf.get("workdir")
    if workdir:
        args.extend(["-w", str(workdir)])

    for key, value in sorted(exec_block["env"].items()):
        args.extend(["-e", f"{key}={value}"])

    secret_names: list[str] = []
    env: dict[str, str] = {}
    for name in conf.get("secrets") or []:
        secret_name = str(name).strip()
        if not _ENV_NAME_RE.fullmatch(secret_name):
            raise TransportError(
                f"{entry_name}: container.secrets entries must be environment variable names, "
                f"got {name!r}"
            )
        # ``-e NAME`` (no value) forwards the variable from the docker client's
        # environment, so the value never appears in argv or the container's
        # process list; the value is placed in the wrapper's environment instead.
        args.extend(["-e", secret_name])
        secret_names.append(secret_name)
        env[secret_name] = _field_value(
            {"secret": secret_name},
            field=f"container.secrets.{secret_name}",
            entry_name=entry_name,
            secret_lookup=secret_lookup,
        )
        notes.append(f"secret {secret_name} forwarded by name (-e {secret_name})")

    args.append(str(conf["image"]))
    args.extend([exec_block["command"], *exec_block["args"]])

    return {
        "transport": "container",
        "command": docker,
        "args": args,
        "env": env,
        "path_prepend": str(Path(docker).parent),
        "secret_names": secret_names,
        "env_from_secrets": {},
        "forwarded_secrets": list(secret_names),
        "notes": notes,
    }


def _plan_vmrun(
    entry_name: str,
    node: dict,
    exec_block: dict,
    *,
    probe_python: Path,
    vmrun_bridge: Path,
    guest_bridge: Path,
    secret_lookup,
) -> dict:
    conf = node.get("vmrun") or {}
    if not isinstance(conf, dict):
        raise TransportError(f"{entry_name}: runner.node.vmrun must be an object")
    if not vmrun_bridge.exists():
        raise TransportError(
            f"{entry_name}: vmrun bridge missing at {vmrun_bridge}; "
            "set registry.policy.node_transports.vmrun_bridge"
        )
    if not guest_bridge.exists():
        raise TransportError(
            f"{entry_name}: node bridge missing at {guest_bridge}; "
            "set registry.policy.node_transports.guest_bridge"
        )

    vmx = conf.get("vmx") or {"secret": "VM_VMX"}
    guest_user = conf.get("guest_user") or {"secret": "VM_GU"}
    guest_password = conf.get("guest_password") or {"secret": "VM_GP"}

    args: list[str] = [str(vmrun_bridge)]
    args.extend(["--vmrun", str(conf.get("vmrun") or DEFAULT_VMRUN)])
    secret_names: list[str] = []
    # Node credentials and the VMX path stay in the wrapper's environment (never on
    # argv, where the host's process list would expose them): the bridge reads the
    # named variables itself, and the guest never receives any of them.
    env: dict[str, str] = {}
    for field, value in (("vmx", vmx), ("guest-user", guest_user), ("guest-password", guest_password)):
        name = _secret_name(value, field=f"vmrun.{field}", entry_name=entry_name)
        if name:
            secret_names.append(name)
            env[name] = _field_value(
                value,
                field=f"vmrun.{field}",
                entry_name=entry_name,
                secret_lookup=secret_lookup,
            )
            args.extend([f"--{field}-env", name])
        else:
            args.append(f"--{field}")
            args.append(
                _field_value(value, field=f"vmrun.{field}", entry_name=entry_name)
            )

    args.extend(["--guest-dir", str(conf.get("guest_dir") or GUEST_DIR_WINDOWS)])
    args.extend(["--guest-python", str(conf.get("guest_python") or DEFAULT_GUEST_PYTHON)])
    args.extend(["--guest-bridge", str(guest_bridge)])
    args.extend(
        [
            "--exec-argv",
            json.dumps([exec_block["command"], *exec_block["args"]], ensure_ascii=False),
        ]
    )
    if exec_block["env"]:
        args.extend(["--exec-env", json.dumps(exec_block["env"], ensure_ascii=False)])
    if exec_block["cwd"]:
        args.extend(["--exec-cwd", exec_block["cwd"]])
    args.extend(
        [
            "--poll",
            _int_field(conf, "poll_interval", DEFAULT_POLL_INTERVAL, entry_name=entry_name, field="vmrun.poll_interval"),
            "--idle",
            _int_field(conf, "idle_seconds", DEFAULT_IDLE_SECONDS, entry_name=entry_name, field="vmrun.idle_seconds"),
            "--copy-timeout",
            _int_field(conf, "copy_timeout", DEFAULT_COPY_TIMEOUT, entry_name=entry_name, field="vmrun.copy_timeout"),
            "--response-timeout",
            _int_field(
                conf,
                "response_timeout",
                DEFAULT_RESPONSE_TIMEOUT,
                entry_name=entry_name,
                field="vmrun.response_timeout",
            ),
        ]
    )

    if not Path(probe_python).exists():
        raise TransportError(f"{entry_name}: probe interpreter missing at {probe_python}")

    # The vmrun wrapper must run on the host; any interpreter will do because the
    # bridge is stdlib-only, so the probe environment's python is reused.
    return {
        "transport": "vmrun_guest",
        "command": str(probe_python),
        "args": args,
        "env": env,
        "path_prepend": str(Path(probe_python).parent),
        "secret_names": secret_names,
        "env_from_secrets": {},
        "forwarded_secrets": [],
        "notes": [
            "VMware Guest Operations file bridge over VMCI (no guest TCP port)",
            "guest credentials never leave the host gateway process environment",
        ],
    }


def plan_launch(
    entry: dict,
    *,
    transport: str,
    repo_root: Path,
    probe_python: Path,
    policy: dict,
    guest_bridge: Path,
    vmrun_bridge: Path,
    which=shutil.which,
    secret_lookup=None,
) -> dict:
    """Build the launch plan for a node transport.

    Returns ``{'transport', 'command', 'args', 'env', 'path_prepend',
    'secret_names', 'forwarded_secrets', 'notes'}``. ``command``/``args`` spawn a
    stdio wrapper and ``env`` is the environment it needs; ``secret_names`` are the
    variables the *wrapper* consumed, and ``forwarded_secrets`` lists the names (a
    subset) whose values cross into the node itself.

    ``secret_lookup`` resolves a ``{"secret": "NAME"}`` reference (and is expected
    to raise for a missing name). Pass ``None`` for the describe path: fields then
    render as ``<NAME>``, so a plan is printable, loggable and value-free.
    """
    entry_name = entry.get("name", "?")
    if transport == "stdio_local":
        raise TransportError(
            f"{entry_name}: stdio_local is planned from the registry entry's runner block; "
            "mcp_transports only plans node transports"
        )
    node = node_block(entry)
    if not node:
        raise TransportError(
            f"{entry_name}: transport {transport!r} needs a runner.node block "
            "(ssh/container/vmrun addressing, exec argv and probe_env)"
        )
    exec_block = _exec_block(node, entry_name)

    if transport == "ssh":
        plan = _plan_ssh(entry_name, node, exec_block, which=which, secret_lookup=secret_lookup)
    elif transport == "container":
        plan = _plan_container(
            entry_name,
            node,
            exec_block,
            repo_root=Path(repo_root),
            which=which,
            secret_lookup=secret_lookup,
        )
    elif transport == "vmrun_guest":
        plan = _plan_vmrun(
            entry_name,
            node,
            exec_block,
            probe_python=Path(probe_python),
            vmrun_bridge=Path(vmrun_bridge),
            guest_bridge=Path(guest_bridge),
            secret_lookup=secret_lookup,
        )
    else:  # pragma: no cover - transport_for already validates the value
        raise TransportError(f"{entry_name}: unknown transport {transport!r}")

    plan["exec"] = exec_block
    plan.setdefault("forwarded_secrets", [])
    plan.setdefault("env", {})
    plan.setdefault("env_from_secrets", {})
    plan["path_prepend"] = plan.get("path_prepend") or str(Path(plan["command"]).parent)
    return plan


def describe(plan: dict, *, repo_root: Path | None = None) -> str:
    """One-line, value-free summary of a plan (safe to print and to log)."""

    def _display(path: str) -> str:
        candidate = Path(path)
        if repo_root is not None:
            try:
                return candidate.resolve().relative_to(Path(repo_root).resolve()).as_posix()
            except (ValueError, OSError):
                pass
        return str(path)

    argv = " ".join(shlex.quote(_display(item) if os.path.isabs(item) else item) for item in plan["args"])
    secrets = ",".join(plan["secret_names"]) or "-"
    return f"transport={plan['transport']} command={_display(plan['command'])} secrets={secrets}\n  argv: {argv}"
