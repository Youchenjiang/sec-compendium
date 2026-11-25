import contextlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import collab_protocol as protocol
import collab_watch


TASK_BODY = """# TASK: T001

- **所屬大題**：`C01_Test`
- **關聯小題**：`Q01`
- **任務類型**：`TRIAGE`
- **Protocol Contract**：`v2.3`
- **Target Role**：`ROLE_01_TRIAGE_HUNTER`
- **Assignee Session**：`Session-Worker`
- **發起 Session**：`Session-Lead`
- **Execution Environment**：`portable_text_any`
- **Task ID**：`T001`
"""


class _TransportHarness:
    def __init__(self, root: Path):
        self.root = root
        self.cases = root / ".collab" / "cases"
        self.events = root / ".collab" / "runtime" / "events"
        self.inbox = root / ".collab" / "runtime" / "inbox"
        self.case = self.cases / "C01_Test"
        for child in ("tasks", "findings", "reviews"):
            (self.case / child).mkdir(parents=True, exist_ok=True)
        (self.case / "CASE_STATE.md").write_text(
            "# State\n- **主導代理人 (Lead Session)**：`Session-Lead`\n",
            encoding="utf-8",
        )
        (self.case / "tasks" / "T001_TRIAGE.md").write_text(
            TASK_BODY, encoding="utf-8"
        )

    def patches(self):
        return [
            patch.object(protocol, "REPO_ROOT", self.root),
            patch.object(protocol, "CASES_DIR", self.cases),
            patch.object(protocol, "EVENTS_DIR", self.events),
            patch.object(protocol, "INBOX_DIR", self.inbox),
            patch.object(collab_watch, "CASES_DIR", self.cases),
            patch.object(collab_watch, "copy_to_clipboard"),
            patch.object(collab_watch, "beep"),
        ]

    def run_assignment(self, **kwargs):
        state_path = self.root / ".collab" / "runtime" / "watchers" / "Session-Worker.json"
        state = {"seen_tasks": set(), "seen_events": set()}
        task_path = self.case / "tasks" / "T001_TRIAGE.md"
        if not protocol.events_for_task("C01_Test", "T001"):
            protocol.emit_event(
                kind="DISPATCHED",
                case_id="C01_Test",
                task_id="T001",
                from_session="Session-Lead",
                to_session="Session-Worker",
                task_path=task_path,
            )
        return collab_watch.process_assignments(
            session="Session-Worker",
            case_filters={"C01_Test"},
            state=state,
            state_path=state_path,
            **kwargs,
        )


class HandoffTransportTests(unittest.TestCase):
    def _with_patches(self, root, func):
        harness = _TransportHarness(root)
        with contextlib.ExitStack() as stack:
            for patcher in harness.patches():
                stack.enter_context(patcher)
            return func(harness)

    def test_file_transport_writes_handoff_and_acks(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._with_patches(
                Path(tmp),
                lambda h: (
                    h.run_assignment(
                        exec_program=None, exec_args=[], transport="file"
                    ),
                    list(protocol.iter_handoffs("Session-Worker")),
                    [
                        payload["kind"]
                        for _, payload in protocol.incoming_events("Session-Lead")
                    ],
                ),
            )
            announced, handoffs, to_lead = result

        self.assertEqual(announced, 1)
        self.assertEqual(len(handoffs), 1)
        _, handoff = handoffs[0]
        self.assertEqual(handoff["schema"], "collab-handoff/v1")
        self.assertEqual(handoff["transport"], "file")
        self.assertEqual(handoff["lead_session"], "Session-Lead")
        self.assertTrue(handoff["required_commands"])
        self.assertIn("ACK", to_lead)

    def test_agent_failure_falls_back_to_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._with_patches(
                Path(tmp),
                lambda h: (
                    h.run_assignment(
                        exec_program=sys.executable,
                        exec_args=["-c", "import sys; sys.exit(3)"],
                        transport="agent",
                        exec_timeout=30,
                    ),
                    list(protocol.iter_handoffs("Session-Worker")),
                    [
                        payload["kind"]
                        for _, payload in protocol.incoming_events("Session-Lead")
                    ],
                ),
            )
            announced, handoffs, to_lead = result

        self.assertEqual(announced, 1)
        self.assertEqual(len(handoffs), 1)
        _, handoff = handoffs[0]
        self.assertEqual(handoff["transport"], "agent")
        self.assertIn("ACK", to_lead)

    def test_agent_success_still_writes_durable_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._with_patches(
                Path(tmp),
                lambda h: (
                    h.run_assignment(
                        exec_program=sys.executable,
                        exec_args=["-c", "import sys; sys.exit(0)"],
                        transport="agent",
                        exec_timeout=30,
                    ),
                    list(protocol.iter_handoffs("Session-Worker")),
                ),
            )
            announced, handoffs = result

        self.assertEqual(announced, 1)
        self.assertEqual(len(handoffs), 1)

    def test_second_fresh_watcher_does_not_relaunch_same_assignment(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            harness = _TransportHarness(root)
            with contextlib.ExitStack() as stack:
                for patcher in harness.patches():
                    stack.enter_context(patcher)
                first = harness.run_assignment(
                    exec_program=None, exec_args=[], transport="file"
                )
                with patch.object(collab_watch, "dispatch_cli") as dispatch:
                    second = harness.run_assignment(
                        exec_program=sys.executable,
                        exec_args=[],
                        transport="agent",
                        exec_timeout=30,
                    )
                self.assertEqual(first, 1)
                self.assertEqual(second, 0)
                dispatch.assert_not_called()

    def test_fresh_watcher_recovers_active_task_when_handoff_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            harness = _TransportHarness(root)
            with contextlib.ExitStack() as stack:
                for patcher in harness.patches():
                    stack.enter_context(patcher)
                first = harness.run_assignment(
                    exec_program=None, exec_args=[], transport="file"
                )
                self.assertEqual(first, 1)
                handoff = protocol.handoff_path_for_task(
                    "Session-Worker", "C01_Test", "T001"
                )
                handoff.unlink()
                output = harness.case / "findings" / "FINDING_T001.md"
                output.write_text("# partial output\n", encoding="utf-8")

                recovered = harness.run_assignment(
                    exec_program=None, exec_args=[], transport="file"
                )
                self.assertEqual(recovered, 1)
                self.assertTrue(handoff.exists())
                payload = next(protocol.iter_handoffs("Session-Worker"))[1]
                self.assertFalse(
                    any("init-output" in command for command in payload["required_commands"])
                )

    def test_host_local_gateway_rejects_remote_node_and_accepts_primary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            harness = _TransportHarness(root)
            task = harness.case / "tasks" / "T001_TRIAGE.md"
            task.write_text(
                TASK_BODY.replace(
                    "- **Execution Environment**：`portable_text_any`\n",
                    "- **Execution Environment**：`host_local_gateway`\n",
                ),
                encoding="utf-8",
            )
            with contextlib.ExitStack() as stack:
                for patcher in harness.patches():
                    stack.enter_context(patcher)
                with self.assertRaisesRegex(ValueError, "requires host_local_gateway"):
                    harness.run_assignment(
                        exec_program=None,
                        exec_args=[],
                        transport="file",
                        node_class="remote",
                    )
                announced = harness.run_assignment(
                    exec_program=None,
                    exec_args=[],
                    transport="file",
                    node_class="primary",
                )
                self.assertEqual(announced, 1)

    def test_mutated_execution_environment_is_rejected_before_routing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            harness = _TransportHarness(root)
            task = harness.case / "tasks" / "T001_TRIAGE.md"
            original = TASK_BODY.replace(
                "- **Execution Environment**：`portable_text_any`\n",
                "- **Execution Environment**：`host_local_gateway`\n",
            )
            task.write_text(original, encoding="utf-8")
            with contextlib.ExitStack() as stack:
                for patcher in harness.patches():
                    stack.enter_context(patcher)
                protocol.emit_event(
                    kind="DISPATCHED",
                    case_id="C01_Test",
                    task_id="T001",
                    from_session="Session-Lead",
                    to_session="Session-Worker",
                    task_path=task,
                )
                task.write_text(TASK_BODY, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "immutable task hash 已改變"):
                    harness.run_assignment(
                        exec_program=None,
                        exec_args=[],
                        transport="file",
                        node_class="remote",
                    )
                kinds = [
                    payload["kind"]
                    for _, payload in protocol.events_for_task("C01_Test", "T001")
                ]
                self.assertEqual(kinds, ["DISPATCHED"])

    def test_auto_node_class_is_fail_closed(self):
        with patch.dict(collab_watch.os.environ, {}, clear=True):
            self.assertEqual(collab_watch.resolve_node_class("auto"), "remote")
        with patch.dict(
            collab_watch.os.environ, {"COLLAB_NODE_CLASS": "primary"}, clear=True
        ):
            self.assertEqual(collab_watch.resolve_node_class("auto"), "primary")

    def test_dispatch_cli_times_out_without_hanging(self):
        exit_code = collab_watch.dispatch_cli(
            sys.executable,
            ["-c", "import time; time.sleep(5)"],
            "noop",
            timeout=0.5,
        )
        self.assertEqual(exit_code, 124)

    def test_write_handoff_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            case_dir = root / "C01_Test"
            case_dir.mkdir(parents=True)
            task = case_dir / "T001_TRIAGE.md"
            output = case_dir / "FINDING_T001.md"
            task.write_text("# TASK: T001\n", encoding="utf-8")
            task.write_text(TASK_BODY, encoding="utf-8")
            with patch.object(protocol, "REPO_ROOT", root), patch.object(
                protocol, "INBOX_DIR", root / "inbox"
            ):
                path = protocol.write_handoff(
                    session="Session-Worker",
                    task=protocol.HandoffTask(
                        case_id="C01_Test",
                        task_id="T001",
                        task_type="TRIAGE",
                        execution_environment="portable_text_any",
                        task_path=task,
                        output_path=output,
                    ),
                    current_state="ACK",
                    instruction="do the thing",
                    reason="test",
                    transport="file",
                    lead_session="Session-Lead",
                )
                listed = list(protocol.iter_handoffs("Session-Worker"))
                self.assertTrue(path.exists())
                self.assertEqual(len(listed), 1)
                self.assertEqual(listed[0][1]["task_id"], "T001")

    def test_review_handoff_uses_review_ready_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task = root / "T002_REVIEW.md"
            output = root / "REVIEW_T002.md"
            task.write_text("# TASK: T002\n", encoding="utf-8")
            with patch.object(protocol, "REPO_ROOT", root), patch.object(
                protocol, "INBOX_DIR", root / "inbox"
            ):
                path = protocol.write_handoff(
                    session="Session-Reviewer",
                    task=protocol.HandoffTask(
                        case_id="C01_Test",
                        task_id="T002",
                        task_type="REVIEW",
                        execution_environment="portable_text_any",
                        task_path=task,
                        output_path=output,
                    ),
                    current_state="ACK",
                    instruction="review the finding",
                    reason="test",
                    transport="file",
                    lead_session="Session-Lead",
                )
                payload = next(
                    payload
                    for handoff_path, payload in protocol.iter_handoffs("Session-Reviewer")
                    if handoff_path == path
                )
                self.assertIn("review ready", payload["required_commands"][-1])
                self.assertNotIn("finding ready", payload["required_commands"][-1])

    def test_iter_handoffs_empty_returns_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(protocol, "INBOX_DIR", Path(tmp) / "inbox"):
                self.assertEqual(list(protocol.iter_handoffs("Session-None")), [])


class SyncArtifactTests(unittest.TestCase):
    def test_is_sync_artifact_markers(self):
        self.assertTrue(protocol.is_sync_artifact(Path("T900 (conflicted copy).json")))
        self.assertTrue(protocol.is_sync_artifact(Path("T900 (conflicted copy 2026-09-26).json")))
        self.assertTrue(protocol.is_sync_artifact(Path("Session-Worker (Joe's conflicted copy).json")))
        self.assertTrue(protocol.is_sync_artifact(Path(".T900.json.tmp-deadbeef")))
        self.assertTrue(protocol.is_sync_artifact(Path("T900.json~")))
        self.assertFalse(protocol.is_sync_artifact(Path("T900.json")))
        self.assertFalse(protocol.is_sync_artifact(Path("Session-Conflict-Reviewer.json")))

    def test_iter_handoffs_ignores_conflict_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            case_dir = root / "C01_Test"
            case_dir.mkdir(parents=True)
            task = case_dir / "T001_TRIAGE.md"
            output = case_dir / "FINDING_T001.md"
            task.write_text("# TASK: T001\n", encoding="utf-8")
            task.write_text(TASK_BODY, encoding="utf-8")
            with patch.object(protocol, "REPO_ROOT", root), patch.object(
                protocol, "INBOX_DIR", root / "inbox"
            ):
                path = protocol.write_handoff(
                    session="Session-Worker",
                    task=protocol.HandoffTask(
                        case_id="C01_Test",
                        task_id="T001",
                        task_type="TRIAGE",
                        execution_environment="portable_text_any",
                        task_path=task,
                        output_path=output,
                    ),
                    current_state="ACK",
                    instruction="do the thing",
                    reason="test",
                    transport="file",
                    lead_session="Session-Lead",
                )
                conflict = path.with_name("T001 (conflicted copy).json")
                conflict.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
                handoffs = list(protocol.iter_handoffs("Session-Worker"))
                artifacts = list(protocol.iter_sync_artifacts(root / "inbox"))

        self.assertEqual(len(handoffs), 1)
        self.assertEqual(handoffs[0][1]["task_id"], "T001")
        self.assertEqual(len(artifacts), 1)
        self.assertEqual(artifacts[0].name, "T001 (conflicted copy).json")

    def test_iter_events_ignores_conflict_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            events = root / "events"
            case_dir = root / "cases" / "C01_Test"
            case_dir.mkdir(parents=True)
            task = case_dir / "T001_TRIAGE.md"
            task.write_text("# TASK\n", encoding="utf-8")
            with patch.object(protocol, "REPO_ROOT", root), patch.object(
                protocol, "EVENTS_DIR", events
            ):
                protocol.emit_event(
                    kind="DISPATCHED",
                    case_id="C01_Test",
                    task_id="T001",
                    from_session="Session-Lead",
                    to_session="Session-Worker",
                    task_path=task,
                )
                target_dir = protocol.event_dir("C01_Test", "T001")
                original = next(target_dir.glob("*.json"))
                (target_dir / "DISPATCHED (conflicted copy).json").write_text(
                    original.read_text(encoding="utf-8"), encoding="utf-8"
                )
                events_found = list(protocol.iter_events())
                task_events = protocol.events_for_task("C01_Test", "T001")

        self.assertEqual(len(events_found), 1)
        self.assertEqual(len(task_events), 1)


if __name__ == "__main__":
    unittest.main()
