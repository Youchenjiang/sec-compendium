import contextlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import collab_host_watch
import collab_protocol as protocol
import collab_watch


TASK_BODY = """# TASK: {task_id}

- **所屬大題**：`C01_Test`
- **關聯小題**：`Q01`
- **任務類型**：`{task_type}`
- **Protocol Contract**：`v2.3`
- **Target Role**：`ROLE_01_TRIAGE_HUNTER`
- **Assignee Session**：`{session}`
- **發起 Session**：`Session-Lead`
- **Execution Environment**：`portable_text_any`
- **Task ID**：`{task_id}`
"""


class _HostHarness:
    """A minimal governed tree rooted in a temp dir, mimicking host 2's view."""

    def __init__(self, root: Path, *, lead: str = "Session-Lead"):
        self.root = root
        self.cases = root / ".collab" / "cases"
        self.events = root / ".collab" / "runtime" / "events"
        self.inbox = root / ".collab" / "runtime" / "inbox"
        self.watchers = root / ".collab" / "runtime" / "watchers"
        self.case = self.cases / "C01_Test"
        for child in ("tasks", "findings", "reviews"):
            (self.case / child).mkdir(parents=True, exist_ok=True)
        (self.case / "CASE_STATE.md").write_text(
            f"# State\n- **主導代理人 (Lead Session)**：`{lead}`\n", encoding="utf-8"
        )

    def add_task(self, task_id: str, session: str, *, task_type: str = "TRIAGE") -> Path:
        path = self.case / "tasks" / f"{task_id}_{task_type}.md"
        path.write_text(
            TASK_BODY.format(task_type=task_type, session=session, task_id=task_id),
            encoding="utf-8",
        )
        protocol.emit_event(
            kind="DISPATCHED",
            case_id="C01_Test",
            task_id=task_id,
            from_session="Session-Lead",
            to_session=session,
            task_path=path,
        )
        return path

    def patches(self):
        return [
            patch.object(protocol, "REPO_ROOT", self.root),
            patch.object(protocol, "CASES_DIR", self.cases),
            patch.object(protocol, "EVENTS_DIR", self.events),
            patch.object(protocol, "INBOX_DIR", self.inbox),
            patch.object(collab_watch, "CASES_DIR", self.cases),
            patch.object(collab_watch, "RUNTIME_DIR", self.watchers),
            patch.object(collab_watch, "copy_to_clipboard"),
            patch.object(collab_watch, "beep"),
        ]


def _supervisor(harness: _HostHarness, **kwargs) -> collab_host_watch.HostWatchSupervisor:
    kwargs.setdefault("prefix", "Session-H2-")
    kwargs.setdefault("case_filters", {"C01_Test"})
    return collab_host_watch.HostWatchSupervisor(**kwargs)


class DiscoverHostSessionsTests(unittest.TestCase):
    def test_only_prefix_matched_assignees_are_host_owned(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = _HostHarness(Path(tmp))
            with contextlib.ExitStack() as stack:
                for ctx in harness.patches():
                    stack.enter_context(ctx)
                harness.add_task("T001", "Session-H2-CodeAuditor")
                harness.add_task("T002", "Session-H1-Reverse")
                harness.add_task("T003", "Session-H2-WebAnalyst")
                harness.add_task("T004", "Session-CoS-Triage")

                sessions = collab_host_watch.discover_host_sessions(
                    prefix="Session-H2-"
                )

        self.assertEqual(
            sessions, ["Session-H2-CodeAuditor", "Session-H2-WebAnalyst"]
        )

    def test_prior_watcher_state_and_inbox_keep_a_session_visible(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = _HostHarness(Path(tmp))
            with contextlib.ExitStack() as stack:
                for ctx in harness.patches():
                    stack.enter_context(ctx)
                # No task currently references this session, but it ran before.
                harness.watchers.mkdir(parents=True, exist_ok=True)
                (harness.watchers / "Session-H2-WebAnalyst.json").write_text(
                    "{}", encoding="utf-8"
                )
                (harness.inbox / "Session-H2-SmartContract" / "C01_Test").mkdir(
                    parents=True
                )

                sessions = collab_host_watch.discover_host_sessions(
                    prefix="Session-H2-"
                )

        self.assertEqual(
            sessions, ["Session-H2-SmartContract", "Session-H2-WebAnalyst"]
        )


class SupervisorSweepTests(unittest.TestCase):
    def test_sweep_acks_and_queues_handoff_for_host_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = _HostHarness(Path(tmp))
            with contextlib.ExitStack() as stack:
                for ctx in harness.patches():
                    stack.enter_context(ctx)
                harness.add_task("T001", "Session-H2-CodeAuditor")
                harness.add_task("T002", "Session-H1-Reverse")

                supervisor = _supervisor(harness)
                sessions = supervisor.sweep()

                payloads = [
                    payload
                    for _, payload in protocol.events_for_task("C01_Test", "T001")
                ]
                kinds = {payload["kind"] for payload in payloads}
                ack_actor = next(
                    (
                        payload["from_session"]
                        for payload in payloads
                        if payload["kind"] == "ACK"
                    ),
                    None,
                )
                handoff = (
                    harness.inbox / "Session-H2-CodeAuditor" / "C01_Test" / "T001.json"
                )
                handoff_exists = handoff.is_file()
                state = protocol.latest_task_state("C01_Test", "T001")

        self.assertEqual(sessions, ["Session-H2-CodeAuditor"])
        self.assertIn("ACK", kinds)
        self.assertNotIn("START", kinds)
        self.assertEqual(ack_actor, "Session-H2-CodeAuditor")
        self.assertTrue(handoff_exists)
        self.assertEqual(state, "ACK")
        self.assertEqual(len(supervisor.queued_handoffs), 1)

    def test_worker_command_receives_the_handoff_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = _HostHarness(Path(tmp))
            with contextlib.ExitStack() as stack:
                for ctx in harness.patches():
                    stack.enter_context(ctx)
                harness.add_task("T001", "Session-H2-CodeAuditor")
                worker = [
                    sys.executable,
                    "-c",
                    "import pathlib, sys; pathlib.Path(sys.argv[1] + '.ran').write_text('ok')",
                ]
                supervisor = _supervisor(harness, worker_command=worker)
                supervisor.sweep()

                handoff = (
                    harness.inbox / "Session-H2-CodeAuditor" / "C01_Test" / "T001.json"
                )
                marker_exists = Path(str(handoff) + ".ran").is_file()

        self.assertTrue(marker_exists)

    def test_rescan_discovers_a_newly_dispatched_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = _HostHarness(Path(tmp))
            with contextlib.ExitStack() as stack:
                for ctx in harness.patches():
                    stack.enter_context(ctx)
                harness.add_task("T001", "Session-H2-CodeAuditor")
                supervisor = _supervisor(harness)
                first = supervisor.sessions(force=True)

                harness.add_task("T004", "Session-H2-SmartContract")
                cached = supervisor.sessions()
                refreshed = supervisor.sessions(force=True)

        self.assertEqual(first, ["Session-H2-CodeAuditor"])
        self.assertNotIn("Session-H2-SmartContract", cached)
        self.assertIn("Session-H2-SmartContract", refreshed)

    def test_single_world_task_error_does_not_stop_other_sessions(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = _HostHarness(Path(tmp))
            with contextlib.ExitStack() as stack:
                for ctx in harness.patches():
                    stack.enter_context(ctx)
                harness.add_task("T001", "Session-H2-CodeAuditor")
                harness.add_task("T002", "Session-H2-WebAnalyst")

                supervisor = _supervisor(harness)
                original = supervisor.process_session

                def explode_on_one(session):
                    if session == "Session-H2-CodeAuditor":
                        raise ValueError("simulated gate failure")
                    return original(session)

                supervisor.process_session = explode_on_one  # type: ignore[assignment]
                sessions = supervisor.sweep()

                web_state = protocol.latest_task_state("C01_Test", "T002")

        self.assertEqual(
            sessions, ["Session-H2-CodeAuditor", "Session-H2-WebAnalyst"]
        )
        self.assertEqual(web_state, "ACK")


if __name__ == "__main__":
    unittest.main()
