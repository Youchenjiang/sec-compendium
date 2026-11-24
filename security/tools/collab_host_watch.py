#!/usr/bin/env python3
"""Resident multi-session watcher supervisor for a secondary (worker) host.

Why this exists
---------------
``collab_watch.py`` watches exactly one Session name. That is fine for a Lead
on host 1, but host 2 is a pure worker node: host 1 may route work to *any*
``Session-H2-*`` name, including a brand-new one host 2 has never seen. Running
one hand-started watcher per session does not scale and silently drops tasks
whose assignee nobody happened to launch.

This supervisor fixes that by:

* discovering every host-owned session directly from the governed task tree
  (assignee names matching a prefix such as ``Session-H2-``), plus any prior
  watcher state or queued handoff inbox;
* keeping a watcher pass alive per session, re-scanning so a newly dispatched
  ``Session-H2-Foo`` starts being watched without a restart;
* defaulting to the browser-free ``file`` transport, so ACK + the durable
  handoff packet never depend on an interactive composer (the T900 failure);
* optionally invoking a ``--worker-command`` per freshly queued handoff, so an
  agent wired there turns the handoff into a real finding/review artifact.

It is read-only with respect to host-1 artifacts: it only ACKs exact-assignee
tasks and writes handoff packets below Git-ignored runtime storage.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import collab_protocol as protocol
import collab_watch


DEFAULT_SESSION_PREFIX = "Session-H2-"


def is_host_session(session: str, prefix: str) -> bool:
    """True when a session name belongs to this host (prefix + legal chars)."""
    if not session or not session.startswith(prefix):
        return False
    return bool(protocol.SESSION_RE.fullmatch(session))


def discover_host_sessions(
    *,
    prefix: str = DEFAULT_SESSION_PREFIX,
    case_filters: set[str] | None = None,
    cases_dir: Path | None = None,
    watchers_dir: Path | None = None,
    inbox_dir: Path | None = None,
) -> list[str]:
    """Return all host-owned session names, sorted and de-duplicated.

    Sessions are collected from the task tree (so a freshly dispatched
    assignment is seen immediately), from prior watcher state, and from queued
    handoff inboxes (so a session stays watched across tasks).
    """
    cases_dir = cases_dir or collab_watch.CASES_DIR
    watchers_dir = watchers_dir or collab_watch.RUNTIME_DIR
    inbox_dir = inbox_dir or protocol.INBOX_DIR

    sessions: set[str] = set()

    for task_path in protocol.iter_tasks(cases_dir, case_filters) or []:
        assignee = protocol.parse_task_metadata(task_path).get("assignee_session", "")
        if is_host_session(assignee, prefix):
            sessions.add(assignee)

    if watchers_dir.exists():
        for state_path in watchers_dir.glob("*.json"):
            if is_host_session(state_path.stem, prefix):
                sessions.add(state_path.stem)

    if inbox_dir.exists():
        for entry in inbox_dir.iterdir():
            if entry.is_dir() and is_host_session(entry.name, prefix):
                sessions.add(entry.name)

    return sorted(sessions)


class HostWatchSupervisor:
    """Keep a governed watcher pass alive for every host-owned session."""

    def __init__(
        self,
        *,
        prefix: str = DEFAULT_SESSION_PREFIX,
        case_filters: set[str] | None = None,
        interval: float = 2.0,
        rescan_interval: float = 15.0,
        transport: str = "file",
        exec_program: str | None = None,
        exec_args: list[str] | None = None,
        exec_timeout: float = 600.0,
        node_class: str = "auto",
        worker_command: list[str] | None = None,
        watchers_dir: Path | None = None,
        inbox_dir: Path | None = None,
        log_path: Path | None = None,
    ) -> None:
        self.prefix = prefix
        self.case_filters = case_filters
        self.interval = interval
        self.rescan_interval = rescan_interval
        self.transport = transport
        self.exec_program = exec_program
        self.exec_args = list(exec_args or [])
        self.exec_timeout = exec_timeout
        self.node_class = node_class
        self.worker_command = list(worker_command or [])
        self.watchers_dir = watchers_dir or collab_watch.RUNTIME_DIR
        self.inbox_dir = inbox_dir or protocol.INBOX_DIR
        self.log_path = log_path

        self._states: dict[str, dict[str, set[str]]] = {}
        self._sessions: list[str] = []
        self._last_discovery = 0.0
        self.queued_handoffs: list[Path] = []

    # ---- logging ---------------------------------------------------------
    def log(self, message: str) -> None:
        stamp = datetime.now().strftime("%H:%M:%S")
        line = f"[host-watch {stamp}] {message}"
        print(line, flush=True)
        if self.log_path is not None:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            with self.log_path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")

    # ---- watcher wiring --------------------------------------------------
    def _state_path_for(self, session: str) -> Path:
        return self.watchers_dir / f"{session}.json"

    def _state_for(self, session: str) -> dict[str, set[str]]:
        if session not in self._states:
            self._states[session] = collab_watch.load_state(self._state_path_for(session))
        return self._states[session]

    def _on_handoff(self, session: str, handoff_path: Path, instruction: str) -> None:
        self.queued_handoffs.append(handoff_path)
        self.log(
            f"[{session}] handoff queued -> {protocol.relative_posix(handoff_path)}"
        )
        if self.worker_command:
            self.run_worker(handoff_path)
        else:
            self.log(
                f"[{session}] no --worker-command wired; consume with "
                f"`collab_bus.py inbox --session {session} --show`"
            )

    def run_worker(self, handoff_path: Path) -> int:
        """Invoke the configured worker for one handoff packet."""
        command = [*self.worker_command, str(handoff_path)]
        self.log(f"worker: {' '.join(command)}")
        try:
            completed = subprocess.run(
                command, cwd=str(protocol.REPO_ROOT), check=False
            )
        except OSError as exc:
            self.log(f"worker spawn failed: {exc}")
            return 127
        if completed.returncode != 0:
            self.log(f"worker exit={completed.returncode} for {handoff_path.name}")
        return completed.returncode

    def process_session(self, session: str) -> None:
        """Run one poll pass for a single session."""
        state = self._state_for(session)
        state_path = self._state_path_for(session)
        collab_watch.process_assignments(
            session=session,
            case_filters=self.case_filters,
            state=state,
            state_path=state_path,
            exec_program=self.exec_program,
            exec_args=self.exec_args,
            transport=self.transport,
            exec_timeout=self.exec_timeout,
            inbox_dir=self.inbox_dir,
            node_class=self.node_class,
            on_handoff=lambda path, instruction, s=session: self._on_handoff(
                s, path, instruction
            ),
        )
        collab_watch.process_incoming_events(
            session, self.case_filters, state, state_path
        )

    # ---- discovery / sweep ----------------------------------------------
    def sessions(self, *, force: bool = False) -> list[str]:
        now = time.monotonic()
        if force or (now - self._last_discovery) >= self.rescan_interval:
            self._sessions = discover_host_sessions(
                prefix=self.prefix,
                case_filters=self.case_filters,
                watchers_dir=self.watchers_dir,
                inbox_dir=self.inbox_dir,
            )
            self._last_discovery = now
        return self._sessions

    def sweep(self) -> list[str]:
        sessions = self.sessions()
        for session in sessions:
            try:
                self.process_session(session)
            except (OSError, ValueError) as exc:
                # One malformed/gated task must not stop the other sessions.
                self.log(f"[{session}] skipped: {exc}")
        return sessions

    def run(self, *, once: bool = False) -> int:
        self.log(
            f"prefix={self.prefix} transport={self.transport} "
            f"node={collab_watch.resolve_node_class(self.node_class)} "
            f"worker={' '.join(self.worker_command) or '(not configured)'}"
        )
        if once:
            sessions = self.sweep()
            self.log(f"single sweep covered {len(sessions)} session(s)")
            return 0
        self.log("press Ctrl-C to stop")
        try:
            while True:
                self.sweep()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.log("stopped")
            return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Resident watcher supervisor for a worker host (auto-discovers "
        "Session-H2-* assignees and keeps them ACKing and queuing handoffs).",
    )
    parser.add_argument(
        "--prefix",
        default=os.environ.get("COLLAB_HOST_SESSION_PREFIX", DEFAULT_SESSION_PREFIX),
        help=f"session-name prefix owned by this host (default: {DEFAULT_SESSION_PREFIX})",
    )
    parser.add_argument("--case", action="append", dest="cases", default=[])
    parser.add_argument("--interval", type=float, default=2.0, help="poll interval (seconds)")
    parser.add_argument(
        "--rescan-interval",
        type=float,
        default=15.0,
        help="how often to re-discover host sessions (seconds)",
    )
    parser.add_argument("--once", action="store_true", help="run a single sweep and exit")
    parser.add_argument(
        "--list-sessions",
        action="store_true",
        help="print discovered host sessions and exit",
    )
    parser.add_argument(
        "--transport",
        choices=["auto", "agent", "file"],
        default="file",
        help="file (default, browser-free) keeps ACK + handoff independent of a composer",
    )
    parser.add_argument("--exec-program", default=None)
    parser.add_argument("--exec-arg", action="append", default=[])
    parser.add_argument("--exec-timeout", type=float, default=600.0)
    parser.add_argument(
        "--node-class",
        choices=["auto", "primary", "remote"],
        default="auto",
        help="auto uses COLLAB_NODE_CLASS and otherwise defaults remote",
    )
    parser.add_argument(
        "--worker-command",
        default=None,
        help="command run per fresh handoff (the handoff JSON path is appended); "
        "wire an agent CLI here to auto-produce findings",
    )
    parser.add_argument("--worker-arg", action="append", default=[])
    parser.add_argument("--log", default=None, help="also append logs to this file")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.interval <= 0:
        raise SystemExit("--interval 必須大於 0")
    if args.rescan_interval <= 0:
        raise SystemExit("--rescan-interval 必須大於 0")

    worker_command: list[str] = []
    if args.worker_command:
        worker_command = [args.worker_command, *args.worker_arg]

    supervisor = HostWatchSupervisor(
        prefix=args.prefix,
        case_filters=set(args.cases) or None,
        interval=args.interval,
        rescan_interval=args.rescan_interval,
        transport=args.transport,
        exec_program=args.exec_program,
        exec_args=args.exec_arg,
        exec_timeout=args.exec_timeout,
        node_class=args.node_class,
        worker_command=worker_command,
        log_path=Path(args.log) if args.log else None,
    )

    if args.list_sessions:
        sessions = supervisor.sessions(force=True)
        if not sessions:
            print(f"No host sessions match prefix {args.prefix!r}.")
            return 0
        for session in sessions:
            print(session)
        return 0

    return supervisor.run(once=args.once)


if __name__ == "__main__":
    raise SystemExit(main())
