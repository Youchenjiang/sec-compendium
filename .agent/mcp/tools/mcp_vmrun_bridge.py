#!/usr/bin/env python3
r"""Host-side vmrun adapter: exposes a guest MCP server as a local stdio process.

``mcp_probe.py`` - and therefore the entire governed collab path - only knows how
to spawn a stdio child. For a server that belongs inside FLARE-VM this adapter
*is* that child: it forwards every stdin line to the guest and streams the
guest's replies back out, over VMware Guest Operations (VMCI), with no network
port and no SSH service on the guest.

Why a file bridge
-----------------
``vmrun runProgramInGuest`` returns no stdout, and the guest's stdio cannot be
attached across VMCI. Guest Operations *can* copy files, so the session is built
on two files that ``.agent/mcp/tools/mcp_node_bridge.py`` (running inside the
guest) watches:

* ``requests``  : the host appends one JSON-RPC line, then
                  ``CopyFileFromHostToGuest`` pushes the file.
* ``responses`` : the guest appends server stdout lines; the adapter copies the
                  file back with ``CopyFileFromGuestToHost`` and re-emits new
                  complete lines on its own stdout.

Two properties matter for MCP correctness:

* every line is forwarded verbatim, so JSON-RPC framing is preserved;
* a line is only emitted once its trailing newline is present, so a copy landing
  mid-write never yields a truncated message (the line-splitting helper is shared
  with the guest bridge so both sides agree).

Credentials (``-gu``/``-gp``) and the VMX path are read from this process's
environment by default (``VM_GU``/``VM_GP``/``VM_VMX``): the registry stores
variable *names* and ``collab_mcp`` resolves the values from ``secrets.env``.
They are passed only on the host's own ``vmrun`` argv; the guest never sees them.

Usage (normally invoked by ``collab_bus.py mcp tools/call``)::

    python mcp_vmrun_bridge.py --vmrun-exe <vmrun> --vmx-env VM_VMX \
        --guest-user-env VM_GU --guest-password-env VM_GP \
        --guest-dir 'C:\Windows\Temp\mcp-bridge' --guest-python python.exe \
        --guest-bridge .agent/mcp/tools/mcp_node_bridge.py \
        --exec-argv '["python.exe","C:\\Tools\\mcp\\server.py"]'
"""

from __future__ import annotations

import argparse
import json
import os
import queue
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import mcp_node_bridge as node_bridge  # noqa: E402  (shares the line-splitting logic)

SHUTDOWN_SENTINEL = node_bridge.SHUTDOWN_SENTINEL


class BridgeError(RuntimeError):
    """The guest session could not be established or maintained."""


class VmrunClient:
    """Thin, always-timed-out wrapper around ``vmrun`` Guest Operations.

    ``vmrun`` blocks forever on wrong or missing guest credentials, so every call
    carries a timeout. A timeout only kills the host-side ``vmrun`` process, so
    the guest bridge is given ``--idle`` and stops itself rather than lingering
    and holding the guest's temp files (the documented failure mode of raw
    ``vmrun`` calls).
    """

    def __init__(self, vmrun: str, vmx: str, user: str | None, password: str | None, *, timeout: float):
        self.vmrun = vmrun
        self.vmx = vmx
        self.timeout = timeout
        self.auth: list[str] = []
        if user:
            self.auth = ["-gu", user]
            if password is not None:
                self.auth += ["-gp", password]

    def _run(self, args: list[str], *, timeout: float | None = None) -> tuple[int, str, str]:
        cmd = [self.vmrun, "-T", "ws", *self.auth, *args]
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                errors="replace",
                timeout=timeout or self.timeout,
            )
        except FileNotFoundError as exc:
            raise BridgeError(f"vmrun not found: {self.vmrun}") from exc
        except subprocess.TimeoutExpired as exc:
            raise BridgeError(
                f"vmrun timed out after {timeout or self.timeout}s "
                "(most often wrong or missing guest credentials)"
            ) from exc
        return proc.returncode, proc.stdout or "", proc.stderr or ""

    def create_dir(self, guest_dir: str) -> None:
        code, out, err = self._run(["createDirectoryInGuest", self.vmx, guest_dir], timeout=30)
        # An existing directory is a success, but VMware reports that text on
        # *stdout* with a non-zero exit, and ``fileExistsInGuest`` refuses to
        # answer for directories, so the message is the only usable signal.
        detail = f"{out}\n{err}".lower()
        if code != 0 and "already exists" not in detail:
            raise BridgeError(
                f"createDirectoryInGuest failed for {guest_dir}: {(out + ' ' + err).strip()}"
            )

    def delete(self, guest_path: str) -> bool:
        """Best-effort guest file removal (missing files are not an error)."""
        code, _out, _err = self._run(["deleteFileInGuest", self.vmx, guest_path], timeout=20)
        return code == 0

    def put(self, host_path: Path, guest_path: str) -> None:
        code, _out, err = self._run(["CopyFileFromHostToGuest", self.vmx, str(host_path), guest_path])
        if code != 0:
            raise BridgeError(f"CopyFileFromHostToGuest {host_path.name} failed: {err.strip()}")

    def get(self, guest_path: str, host_path: Path) -> None:
        code, _out, err = self._run(["CopyFileFromGuestToHost", self.vmx, guest_path, str(host_path)])
        if code != 0:
            raise BridgeError(f"CopyFileFromGuestToHost {guest_path} failed: {err.strip()}")

    def exists(self, guest_path: str) -> bool:
        code, _out, _err = self._run(["fileExistsInGuest", self.vmx, guest_path], timeout=30)
        return code == 0

    def start(self, program: str, arguments: list[str]) -> None:
        code, out, err = self._run(
            ["runProgramInGuest", self.vmx, "-noWait", program, *arguments], timeout=30
        )
        if code != 0:
            raise BridgeError(f"runProgramInGuest failed: {(out + err).strip()}")


class FileBridge:
    """Pipes MCP messages between this host process and a guest-side bridge."""

    def __init__(
        self,
        client: VmrunClient,
        *,
        guest_dir: str,
        guest_python: str,
        guest_bridge: Path,
        server_argv: list[str],
        server_env: dict[str, str] | None = None,
        server_cwd: str | None = None,
        poll_interval: float = 0.4,
        idle_seconds: float = 120.0,
        copy_timeout: float = 60.0,
    ):
        self.client = client
        self.guest_dir = guest_dir.rstrip("/\\")
        self.guest_python = guest_python
        self.guest_bridge = guest_bridge
        self.poll_interval = poll_interval
        self.idle_seconds = idle_seconds
        self.copy_timeout = copy_timeout
        self.local = Path(tempfile.mkdtemp(prefix="mcp-vmrun-"))
        self.requests_local = self.local / "requests.jsonl"
        self.config_local = self.local / "bridge-config.json"
        self.responses_local = self.local / "responses.jsonl.fetched"
        self.stderr_local = self.local / "responses.jsonl.fetched.stderr"
        self.requests_local.write_text("", encoding="utf-8")
        self.guest_requests = self.guest_join("requests.jsonl")
        self.guest_responses = self.guest_join("responses.jsonl")
        self.guest_ready = self.guest_join("ready.txt")
        self.guest_bridge_path = self.guest_join("mcp_node_bridge.py")
        self.guest_config = self.guest_join("bridge-config.json")
        self.offset = 0
        self.last_output = time.monotonic()
        self._started = False
        self._server_argv = [str(item) for item in server_argv]
        self._server_env = {str(k): str(v) for k, v in (server_env or {}).items()}
        self._server_cwd = server_cwd

    def guest_join(self, name: str) -> str:
        """Join onto the guest directory using the separator *that guest* expects.

        A Windows guest is addressed with drive-letter paths, a Linux guest with
        POSIX ones, so the separator follows the directory rather than the host
        this adapter happens to run on.
        """
        separator = "/" if self.guest_dir.startswith("/") else "\\"
        return f"{self.guest_dir}{separator}{name}"

    # -- setup -----------------------------------------------------------------
    def start(self) -> None:
        """Stage the bridge plus the server argv in the guest, then start it."""
        if self._started:
            return
        # vmrun does not quote guest arguments reliably, so the launch description
        # is staged as a file and the guest gets one simple argument. Passing the
        # argv inline instead fails silently: the guest program exits before doing
        # anything and runProgramInGuest still reports success.
        self.config_local.write_text(
            json.dumps(
                {
                    "argv": self._server_argv,
                    "requests": self.guest_requests,
                    "responses": self.guest_responses,
                    "idle": self.idle_seconds,
                    "ready_file": self.guest_ready,
                    "env": self._server_env,
                    "cwd": self._server_cwd or "",
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        try:
            self.client.create_dir(self.guest_dir)
            # Clear anything a previous, crashed session left behind: a stale
            # responses file would otherwise be replayed into this MCP session.
            for stale in (self.guest_responses, f"{self.guest_responses}.stderr", self.guest_ready):
                self.client.delete(stale)
            self.client.put(self.guest_bridge, self.guest_bridge_path)
            self.client.put(self.requests_local, self.guest_requests)
            self.client.put(self.config_local, self.guest_config)
        except BridgeError as exc:
            raise BridgeError(
                f"{exc} (staging into {self.guest_dir}; check the guest path and that "
                "VMware Tools is running and the guest credentials are correct)"
            ) from exc

        guest_argv = [self.guest_bridge_path, "--config", self.guest_config]
        try:
            self.client.start(self.guest_python, guest_argv)
        except BridgeError as exc:
            raise BridgeError(
                f"{exc} (guest program {self.guest_python!r}: vmrun does not do a PATH "
                "lookup, so a guest needs an absolute interpreter path such as "
                "/usr/bin/python3 or C:\\Python311\\python.exe)"
            ) from exc
        self._started = True
        # The guest bridge writes ready.txt once the server process exists. Waiting
        # for it is what turns "the server never started" into a clear error: a
        # failed guest launch otherwise leaves a session that hangs to its timeout.
        deadline = time.monotonic() + self.copy_timeout
        while time.monotonic() < deadline:
            try:
                if self.client.exists(self.guest_ready):
                    return
            except BridgeError:
                break
            time.sleep(min(self.poll_interval * 3, 2.0))
        tail = self.stderr_tail()
        raise BridgeError(
            f"guest bridge never reported ready in {self.copy_timeout:.0f}s "
            f"(staged at {self.guest_dir}): the guest launch failed, most often because "
            f"the guest program {self.guest_python!r} is not an absolute path or the "
            f"guest cannot write to that directory"
            + (f"\n--- guest bridge log tail ---\n{tail}" if tail else "")
        )

    # -- protocol --------------------------------------------------------------
    def send(self, line: str) -> None:
        """Append one request line and push the requests file to the guest."""
        with self.requests_local.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(line.rstrip("\n") + "\n")
        self.client.put(self.requests_local, self.guest_requests)

    def poll(self) -> list[str]:
        """Fetch the responses file and return whatever new complete lines it holds."""
        try:
            self.client.get(self.guest_responses, self.responses_local)
        except BridgeError:
            return []
        lines, self.offset = node_bridge._read_new_lines(str(self.responses_local), self.offset)
        if lines:
            self.last_output = time.monotonic()
        return lines

    def stderr_tail(self, limit: int = 800) -> str:
        """Best-effort fetch of the guest bridge log, for error messages."""
        if not self._started:
            return ""
        try:
            self.client.get(f"{self.guest_responses}.stderr", self.stderr_local)
            text = self.stderr_local.read_text(encoding="utf-8", errors="replace")
        except (BridgeError, OSError):
            return ""
        return text.strip()[-limit:]

    def close(self, *, wait_seconds: float = 15.0) -> None:
        """Ask the guest bridge to exit, drop guest scratch files and the temp dir."""
        if self._started:
            deadline = time.monotonic() + wait_seconds
            try:
                self.send(SHUTDOWN_SENTINEL)
                while time.monotonic() < deadline:
                    if any(line.strip() == SHUTDOWN_SENTINEL for line in self.poll()):
                        break
                    time.sleep(self.poll_interval)
            except BridgeError:
                pass
            # Best-effort: the guest bridge deletes these itself when it exits, and
            # it always gets to run - unlike this process, which the MCP client may
            # terminate at any moment.
            for guest_path in (
                self.guest_bridge_path,
                self.guest_config,
                self.guest_requests,
                self.guest_responses,
                f"{self.guest_responses}.stderr",
                self.guest_ready,
            ):
                try:
                    self.client.delete(guest_path)
                except BridgeError:
                    pass
        try:
            for path in self.local.iterdir():
                path.unlink()
            self.local.rmdir()
        except OSError:
            pass


def _stdin_pump(sink: "queue.Queue[str | None]") -> None:
    for line in sys.stdin:
        sink.put(line)
    sink.put(None)


def run_bridge(args: argparse.Namespace) -> int:
    """Stream stdin -> guest -> stdout until the client closes stdin and the guest goes quiet."""
    server_argv = json.loads(args.exec_argv)
    if not isinstance(server_argv, list) or not server_argv:
        raise BridgeError("--exec-argv must be a non-empty JSON list")
    server_env = json.loads(args.exec_env) if args.exec_env.strip() else {}

    user = args.guest_user or os.environ.get(args.guest_user_env or "")
    password = args.guest_password
    if password is None and args.guest_password_env:
        password = os.environ.get(args.guest_password_env)
    vmx = args.vmx or os.environ.get(args.vmx_env or "")
    if not vmx:
        raise BridgeError(
            f"no VMX path: pass --vmx, or set the variable named by --vmx-env ({args.vmx_env})"
        )
    if not user or password is None:
        raise BridgeError(
            "guest credentials missing: set the variables named by --guest-user-env / "
            "--guest-password-env (the registry records names; values live in secrets.env)"
        )

    bridge = FileBridge(
        VmrunClient(args.vmrun_exe, vmx, user, password, timeout=float(args.copy_timeout)),
        guest_dir=args.guest_dir,
        guest_python=args.guest_python,
        guest_bridge=Path(args.guest_bridge),
        server_argv=server_argv,
        server_env=server_env,
        server_cwd=args.exec_cwd or None,
        poll_interval=float(args.poll),
        idle_seconds=float(args.idle),
        copy_timeout=float(args.copy_timeout),
    )

    sink: "queue.Queue[str | None]" = queue.Queue()
    threading.Thread(target=_stdin_pump, args=(sink,), name="bridge-stdin", daemon=True).start()

    exit_code = 0
    stdin_open = True
    eof_at: float | None = None
    try:
        bridge.start()
        while True:
            line: str | None = ""
            if stdin_open:
                try:
                    line = sink.get(timeout=bridge.poll_interval)
                except queue.Empty:
                    line = ""
            if line is None:
                stdin_open = False
                eof_at = time.monotonic()
            elif line.strip():
                bridge.send(line)
            for out_line in bridge.poll():
                if out_line.strip() == SHUTDOWN_SENTINEL:
                    return exit_code
                sys.stdout.write(out_line + "\n")
                sys.stdout.flush()
            if not stdin_open and eof_at is not None:
                # Drain: after the client closes stdin, keep polling until the guest
                # has been quiet for ``--drain`` seconds. The quiet timer starts at
                # EOF, never before it - a session's own staging time must not be
                # mistaken for guest silence (that mistake drops the last replies).
                idle = time.monotonic() - max(bridge.last_output, eof_at)
                if idle > float(args.drain) or time.monotonic() - eof_at > float(args.response_timeout):
                    return exit_code
    except BridgeError as exc:
        tail = bridge.stderr_tail()
        detail = f"\n--- guest bridge log tail ---\n{tail}" if tail else ""
        print(f"ERROR {exc}{detail}", file=sys.stderr)
        return 2
    finally:
        bridge.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Expose a guest MCP server as local stdio via vmrun")
    parser.add_argument("--vmrun-exe", default=os.environ.get("VM_VMRUN", "vmrun"))
    parser.add_argument("--vmx", default="")
    parser.add_argument("--vmx-env", default="VM_VMX")
    parser.add_argument("--guest-user", default="")
    parser.add_argument("--guest-user-env", default="VM_GU")
    parser.add_argument("--guest-password", default=None)
    parser.add_argument("--guest-password-env", default="VM_GP")
    parser.add_argument("--guest-dir", required=True)
    parser.add_argument("--guest-python", default="python.exe")
    parser.add_argument("--guest-bridge", required=True)
    parser.add_argument("--exec-argv", required=True, help="server argv on the guest (JSON list)")
    parser.add_argument("--exec-env", default="", help="extra server environment on the guest (JSON object)")
    parser.add_argument("--exec-cwd", default="", help="guest working directory for the server")
    parser.add_argument("--poll", default="0.4")
    parser.add_argument("--idle", default="120")
    parser.add_argument("--copy-timeout", default="60")
    parser.add_argument("--drain", default="2.0", help="seconds of guest silence after EOF before exiting")
    parser.add_argument("--response-timeout", default="120")
    return parser


def _install_shutdown_handlers() -> None:
    """Turn SIGTERM/SIGINT into a normal exit so ``finally: bridge.close()`` runs.

    MCP clients typically *terminate* their stdio child instead of closing stdin.
    Where the host can catch that (POSIX boxes send SIGTERM) the guest bridge is
    told to stop immediately; where it cannot (Windows TerminateProcess), the
    guest bridge's own ``--idle`` timeout is the safety net.
    """

    def _handler(signum, _frame):
        raise SystemExit(0)

    for name in ("SIGTERM", "SIGINT", "SIGBREAK"):
        number = getattr(signal, name, None)
        if number is None:
            continue
        try:
            signal.signal(number, _handler)
        except (OSError, ValueError):
            continue


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    _install_shutdown_handlers()
    try:
        return run_bridge(args)
    except BridgeError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:  # pragma: no cover - interactive only
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
