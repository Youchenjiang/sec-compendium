#!/usr/bin/env python3
"""Node-side stdio bridge: lets a host MCP client drive a server inside a guest.

``vmrun runProgramInGuest`` cannot pipe stdin/stdout across the VMCI channel, so
this script, which runs *inside* the guest next to the server, turns two files
into a pipe:

* ``--requests``  : the host appends one JSON-RPC message per line; we forward
                    every line to the server's stdin.
* ``--responses`` : we append every line the server writes to stdout; the host
                    tails the file and copies it back with
                    ``CopyFileFromGuestToHost``.

Why ``--config`` exists
-----------------------
``vmrun`` does not quote arguments reliably when it hands them to a guest: a JSON
argv (``["python3","/opt/server.py"]``) arrives mangled, the guest program exits
before doing anything, and ``runProgramInGuest`` still reports success. So the
whole launch description - server argv, paths, environment, idle budget - is
staged as a JSON file and the guest is started with a single simple argument,
``--config <file>``. (The same lesson is recorded in ``vmrun_guest.py`` for its
``.cmd`` payloads.)

Notes
-----
* stdlib only, and both a Windows (FLARE-VM) and a POSIX (Linux guest) python can
  run it - a node must not need an install step just to be reachable.
* A line equal to ``__MCP_BRIDGE_SHUTDOWN__`` is a control message: it is never
  forwarded to the server, and it makes this bridge exit. The sentinel is not
  valid JSON, so it cannot collide with a real MCP message.
* The bridge exits after ``--idle`` seconds without new requests, so a host that
  dies cannot leave an orphaned server holding the guest's temp files (the
  documented failure mode of raw ``vmrun`` calls).
* ``--ready-file`` is written once the server process exists; the host waits for
  it, which is the only way to distinguish "running" from "silently did nothing".
* Server stderr goes to ``<responses>.stderr``; without that sink a broken server
  would look like a silent one.
* On the way out the bridge deletes the files the host staged (requests,
  responses, ready, config and itself). The MCP client terminates its child hard
  when a session ends, so the host adapter often has no chance to clean up: the
  guest is the only side that always gets to run.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import time

SHUTDOWN_SENTINEL = "__MCP_BRIDGE_SHUTDOWN__"

#: How long to wait for the server to exit after stdin closes before killing it.
SHUTDOWN_GRACE_SECONDS = 5.0

DEFAULT_IDLE_SECONDS = 120.0

#: How long to leave the staged files in place after announcing the shutdown, so
#: the host has time to observe the sentinel before the files disappear.
DEFAULT_CLEANUP_GRACE_SECONDS = 3.0


def read_new_lines(path: str, offset: int) -> tuple[list[str], int]:
    """Return complete lines appended past ``offset`` plus the byte offset to resume at.

    Reads in binary so the offset is a plain byte count (a text-mode tell() is an
    opaque cookie, and mixing it with length arithmetic breaks on multibyte
    input). A partially written trailing line is deliberately withheld: the other
    side copies these files at arbitrary moments, and a half-written line must
    never reach the MCP client.
    """
    if not os.path.exists(path):
        return [], offset
    with open(path, "rb") as handle:
        handle.seek(offset)
        chunk = handle.read()
    if not chunk:
        return [], offset
    if not chunk.endswith(b"\n"):
        cut = chunk.rfind(b"\n")
        if cut == -1:
            return [], offset
        chunk = chunk[: cut + 1]
    text = chunk.decode("utf-8", errors="replace")
    lines = [line.rstrip("\r") for line in text.split("\n")]
    if lines and lines[-1] == "":
        lines.pop()
    return lines, offset + len(chunk)


# Former private name, kept so existing callers and tests keep working.
_read_new_lines = read_new_lines


def parse_argv(raw) -> list[str]:
    """Decode the server argv: a JSON list, a shell-ish string, or an actual list."""
    if isinstance(raw, list):
        argv = [str(item) for item in raw]
        if not argv:
            raise SystemExit("--argv must not be empty")
        return argv
    raw = (raw or "").strip()
    if not raw:
        raise SystemExit("--argv must not be empty")
    if raw.startswith("["):
        argv = json.loads(raw)
        if not isinstance(argv, list) or not argv:
            raise SystemExit("--argv must be a non-empty JSON list")
        return [str(item) for item in argv]
    import shlex

    return shlex.split(raw)


def staged_path(path: str, what: str = "--config") -> str:
    """Canonical path of a staged file, which must sit next to this bridge script.

    The host stages the config, the request/response/ready files and this script
    into the same guest directory, so a path anywhere else is not one the host
    wrote and is refused.
    """
    staging_dir = os.path.dirname(os.path.realpath(__file__))
    real = os.path.realpath(path)
    if os.path.dirname(real) != staging_dir:
        raise SystemExit(f"{what} must be staged next to the bridge ({staging_dir}): {path}")
    return real


def staged_config_path(path: str) -> str:
    return staged_path(path, "--config")


def load_config(path: str) -> dict:
    """Read the staged launch description written by the host-side bridge."""
    path = staged_config_path(path)
    try:
        # path was confined to the staging directory by staged_config_path above.
        with open(path, "r", encoding="utf-8", errors="replace") as handle:  # skipcq: PTC-W6004
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"cannot read --config {path}: {exc}")
    if not isinstance(data, dict):
        raise SystemExit(f"--config {path} must contain a JSON object")
    return data


def _opt(cli_value, config: dict, key: str, default=None):
    """CLI flag wins over the staged config, which wins over the default."""
    if cli_value not in (None, ""):
        return cli_value
    return config.get(key, default)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Node-side stdio bridge for MCP over vmrun")
    parser.add_argument("--config", default="", help="staged JSON launch description (preferred)")
    parser.add_argument("--argv", default="", help="server command line (JSON list)")
    parser.add_argument("--requests", default="", help="file the host appends requests to")
    parser.add_argument("--responses", default="", help="file the host reads responses from")
    parser.add_argument("--idle", default=None, help="exit after this many idle seconds")
    parser.add_argument("--ready-file", default="", help="file written once the server is up")
    parser.add_argument("--env", default="", help="JSON object of extra server environment")
    parser.add_argument("--cwd", default="", help="guest working directory for the server")
    parser.add_argument(
        "--keep-files",
        action="store_true",
        help="leave the staged files behind on exit (debugging only)",
    )
    parser.add_argument(
        "--cleanup-grace",
        default=None,
        help="seconds to wait after the shutdown sentinel before deleting staged files",
    )
    return parser


def _settings(args: argparse.Namespace) -> dict:
    """Merge CLI flags over the staged config into one launch description."""
    config = load_config(args.config) if args.config else {}
    extra_env = _opt(args.env, config, "env", {})
    if isinstance(extra_env, str):
        extra_env = json.loads(extra_env) if extra_env.strip() else {}
    requests = _opt(args.requests, config, "requests")
    responses = _opt(args.responses, config, "responses")
    ready_file = _opt(args.ready_file, config, "ready_file", "") or ""
    return {
        "server_argv": parse_argv(_opt(args.argv, config, "argv")),
        "requests": staged_path(requests, "--requests") if requests else requests,
        "responses": staged_path(responses, "--responses") if responses else responses,
        "ready_file": staged_path(ready_file, "--ready-file") if ready_file else "",
        "cwd": _opt(args.cwd, config, "cwd", "") or None,
        "idle": float(_opt(args.idle, config, "idle", DEFAULT_IDLE_SECONDS)),
        "cleanup_grace": float(
            _opt(args.cleanup_grace, config, "cleanup_grace", DEFAULT_CLEANUP_GRACE_SECONDS)
        ),
        "keep_files": bool(args.keep_files or config.get("keep_files")),
        "extra_env": extra_env or {},
    }


def _prepare_files(cfg: dict) -> None:
    for path in (cfg["requests"], cfg["responses"], cfg["ready_file"]):
        if path:
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    if not os.path.exists(cfg["requests"]):
        # cfg paths were confined to the staging directory by staged_path in _settings.
        open(cfg["requests"], "a", encoding="utf-8").close()  # skipcq: PTC-W6004
    if os.path.exists(cfg["responses"]):
        os.remove(cfg["responses"])


def _forward(lines: list[str], server, stderr_sink, stopped: threading.Event) -> None:
    """Send request lines to the server; a sentinel or a closed stdin stops the relay."""
    for line in lines:
        if line.strip() == SHUTDOWN_SENTINEL:
            stopped.set()
            return
        if not line.strip():
            continue
        try:
            server.stdin.write(line + "\n")  # type: ignore[union-attr]
            server.stdin.flush()  # type: ignore[union-attr]
        except (BrokenPipeError, ValueError) as exc:
            stderr_sink.write(f"### bridge: server stdin closed: {exc}\n")
            stopped.set()
            return


def _relay_requests(cfg: dict, server, stderr_sink, stopped: threading.Event) -> None:
    """Tail the requests file into the server until stopped or idle for too long."""
    offset = 0
    last_activity = time.monotonic()
    while not stopped.is_set():
        lines, offset = read_new_lines(cfg["requests"], offset)
        if lines:
            last_activity = time.monotonic()
            _forward(lines, server, stderr_sink, stopped)
            time.sleep(0.05)
            continue
        if time.monotonic() - last_activity > cfg["idle"]:
            stderr_sink.write(f"### bridge: idle for {cfg['idle']}s, shutting down\n")
            return
        time.sleep(0.2)


def _stop_server(server, pump: threading.Thread) -> int:
    """Close stdin and reap the server; kill it (exit 3) if it does not stop in time."""
    try:
        server.stdin.close()  # type: ignore[union-attr]
    except (OSError, ValueError):
        pass
    exit_code = 0
    try:
        server.wait(timeout=SHUTDOWN_GRACE_SECONDS)
    except subprocess.TimeoutExpired:
        server.kill()
        exit_code = 3
    pump.join(timeout=SHUTDOWN_GRACE_SECONDS)
    return exit_code


def _run_server(cfg: dict, stderr_sink) -> int:
    env = dict(os.environ)
    env.update({str(key): str(value) for key, value in cfg["extra_env"].items()})
    try:
        server = subprocess.Popen(
            cfg["server_argv"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=stderr_sink,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            env=env,
            cwd=cfg["cwd"],
        )
    except OSError as exc:
        print(f"bridge: cannot start server {cfg['server_argv']!r}: {exc}", file=sys.stderr)
        return 2

    responses = open(cfg["responses"], "a", encoding="utf-8", buffering=1)  # skipcq: PTC-W6004
    stopped = threading.Event()

    def pump_stdout() -> None:
        try:
            for line in server.stdout:  # type: ignore[union-attr]
                responses.write(line if line.endswith("\n") else line + "\n")
                responses.flush()
        finally:
            stopped.set()

    pump = threading.Thread(target=pump_stdout, name="bridge-stdout", daemon=True)
    pump.start()
    if cfg["ready_file"]:
        with open(cfg["ready_file"], "w", encoding="utf-8") as handle:  # skipcq: PTC-W6004
            handle.write(f"{os.getpid()}\n")

    exit_code = 0
    try:
        _relay_requests(cfg, server, stderr_sink, stopped)
    finally:
        # Never leave an orphaned server behind: it would keep holding the
        # guest's temp files, which is exactly what breaks the next session.
        exit_code = _stop_server(server, pump)
        responses.write(SHUTDOWN_SENTINEL + "\n")
        responses.flush()
        responses.close()
        stderr_sink.write("### bridge exit\n")
    return exit_code


def _remove_staged(cfg: dict, config_path: str) -> None:
    # Let the host observe the sentinel first, then remove everything this side
    # staged. The host adapter may already be gone (clients terminate their
    # child rather than closing stdin), so the guest cannot rely on it.
    time.sleep(max(cfg["cleanup_grace"], 0.0))
    for path in (
        cfg["requests"],
        cfg["responses"],
        cfg["responses"] + ".stderr",
        cfg["ready_file"],
        config_path,
        os.path.abspath(__file__),
    ):
        if not path:
            continue
        try:
            os.remove(path)
        except OSError:
            pass


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    cfg = _settings(args)
    if not cfg["requests"] or not cfg["responses"]:
        print("bridge: --requests and --responses (or a --config providing them) are required", file=sys.stderr)
        return 2

    _prepare_files(cfg)
    with open(cfg["responses"] + ".stderr", "a", encoding="utf-8") as stderr_sink:  # skipcq: PTC-W6004
        stderr_sink.write(
            f"### bridge start {time.strftime('%Y-%m-%dT%H:%M:%S')} argv={cfg['server_argv']}\n"
        )
        stderr_sink.flush()
        exit_code = _run_server(cfg, stderr_sink)
        if exit_code == 2:
            return exit_code

    if not cfg["keep_files"]:
        _remove_staged(cfg, args.config)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
