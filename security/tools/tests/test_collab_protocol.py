import json
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import collab_protocol as protocol


TASK_BODY = """# TASK: test

- **所屬大題**：`{case_id}`
- **關聯小題**：`Q02`
- **任務類型**：`{task_type}`
- **Target Role**：`ROLE_01_TRIAGE_HUNTER`
- **Assignee Session**：`{assignee}`
- **發起 Session**：`{issuer}`
- **Task ID**：`{task_id}`
"""


class CollabProtocolTests(unittest.TestCase):
    def build_case(self, root: Path, case_id: str = "C01_Test") -> Path:
        case = root / case_id
        (case / "tasks").mkdir(parents=True)
        (case / "findings").mkdir()
        (case / "reviews").mkdir()
        (case / "CASE_STATE.md").write_text(
            "# State\n- **主導代理人 (Lead Session)**：`Session-Lead`\n",
            encoding="utf-8",
        )
        return case

    def test_get_case_lead(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases = Path(tmp) / "cases"
            self.build_case(cases)
            self.assertEqual(protocol.get_case_lead("C01_Test", cases), "Session-Lead")

    def test_find_task_rejects_duplicate_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases = Path(tmp) / "cases"
            case = self.build_case(cases)
            for name in ("T001_A.md", "T001_B.md"):
                (case / "tasks" / name).write_text(
                    TASK_BODY.format(
                        case_id="C01_Test",
                        task_type="TRIAGE",
                        assignee="Session-A",
                        issuer="Session-Lead",
                        task_id="T001",
                    ),
                    encoding="utf-8",
                )
            with self.assertRaisesRegex(ValueError, "duplicate Task ID"):
                protocol.find_task("C01_Test", "T001", cases)

    def test_discover_exact_assignee_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases = Path(tmp) / "cases"
            case = self.build_case(cases)
            for task_id, assignee in (("T001", "Session-A"), ("T002", "Session-B")):
                (case / "tasks" / f"{task_id}.md").write_text(
                    TASK_BODY.format(
                        case_id="C01_Test",
                        task_type="TRIAGE",
                        assignee=assignee,
                        issuer="Session-Lead",
                        task_id=task_id,
                    ),
                    encoding="utf-8",
                )
            found = protocol.discover_assigned_tasks(cases, "Session-A")
            self.assertEqual([item[1]["task_id"] for item in found], ["T001"])

    def test_runtime_events_are_immutable_files_and_route_by_recipient(self):
        with tempfile.TemporaryDirectory() as tmp:
            events = Path(tmp) / "events"
            first = protocol.emit_event(
                kind="QUESTION",
                case_id="C01_Test",
                task_id="T001",
                from_session="Session-A",
                to_session="Session-Lead",
                message="Need the timezone assumption",
                events_dir=events,
            )
            second = protocol.emit_event(
                kind="REPLY",
                case_id="C01_Test",
                task_id="T001",
                from_session="Session-Lead",
                to_session="Session-A",
                message="Use UTC",
                events_dir=events,
            )

            self.assertNotEqual(first, second)
            incoming = protocol.incoming_events("Session-Lead", events)
            self.assertEqual(len(incoming), 1)
            payload = json.loads(first.read_text(encoding="utf-8"))
            self.assertEqual(payload["kind"], "QUESTION")
            self.assertEqual(payload["to_session"], "Session-Lead")

    def test_latest_task_state_ignores_question_reply(self):
        with tempfile.TemporaryDirectory() as tmp:
            events = Path(tmp) / "events"
            for kind in ("DISPATCHED", "ACK", "QUESTION", "REPLY", "START"):
                protocol.emit_event(
                    kind=kind,
                    case_id="C01_Test",
                    task_id="T001",
                    from_session="Session-A",
                    to_session="Session-Lead",
                    events_dir=events,
                )
            self.assertEqual(
                protocol.latest_task_state("C01_Test", "T001", events), "START"
            )

    def test_latest_task_state_reports_dispatch_failed(self):
        with tempfile.TemporaryDirectory() as tmp:
            events = Path(tmp) / "events"
            for kind in ("DISPATCHED", "NOTE", "DISPATCH_FAILED"):
                protocol.emit_event(
                    kind=kind,
                    case_id="C01_Test",
                    task_id="T001",
                    from_session="Session-Lead",
                    to_session="Session-A",
                    events_dir=events,
                )
            self.assertEqual(
                protocol.latest_task_state("C01_Test", "T001", events),
                "DISPATCH_FAILED",
            )


if __name__ == "__main__":
    unittest.main()
