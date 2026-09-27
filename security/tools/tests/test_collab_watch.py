import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import collab_watch


TASK_BODY = """# TASK: test

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


class CollabWatchTests(unittest.TestCase):
    def test_parse_task_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            task = Path(tmp) / "T001.md"
            task.write_text(
                TASK_BODY.format(
                    task_type="TRIAGE", session="Session-C01-Triage", task_id="T001"
                ),
                encoding="utf-8",
            )
            metadata = collab_watch.parse_task_metadata(task)

        self.assertEqual(metadata["task_type"], "TRIAGE")
        self.assertEqual(metadata["assignee_session"], "Session-C01-Triage")
        self.assertEqual(metadata["execution_environment"], "portable_text_any")
        self.assertEqual(metadata["task_id"], "T001")

    def test_discover_only_exact_assignee_and_skip_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases = root / "cases"
            events = root / "events"
            tasks = cases / "C01_Test" / "tasks"
            template_tasks = cases / "C00_Template" / "tasks"
            tasks.mkdir(parents=True)
            template_tasks.mkdir(parents=True)

            task_a = tasks / "T001.md"
            task_a.write_text(
                TASK_BODY.format(
                    task_type="TRIAGE", session="Session-A", task_id="T001"
                ),
                encoding="utf-8",
            )
            task_b = tasks / "T002.md"
            task_b.write_text(
                TASK_BODY.format(
                    task_type="REVERSE", session="Session-B", task_id="T002"
                ),
                encoding="utf-8",
            )
            (tasks / "README.md").write_text("# Tasks\n", encoding="utf-8")
            (template_tasks / "TASK_TEMPLATE.md").write_text(
                TASK_BODY.format(
                    task_type="TRIAGE", session="Session-A", task_id="T000"
                ),
                encoding="utf-8",
            )

            with patch.object(collab_watch.protocol, "REPO_ROOT", root):
                for task, task_id, assignee in (
                    (task_a, "T001", "Session-A"),
                    (task_b, "T002", "Session-B"),
                ):
                    collab_watch.protocol.emit_event(
                        kind="DISPATCHED",
                        case_id="C01_Test",
                        task_id=task_id,
                        from_session="Session-Lead",
                        to_session=assignee,
                        task_path=task,
                        events_dir=events,
                    )
                found = collab_watch.discover_assigned_tasks(
                    cases, "Session-A", events_dir=events
                )

        self.assertEqual(len(found), 1)
        self.assertEqual(found[0][0].name, "T001.md")
        self.assertEqual(found[0][1]["task_id"], "T001")

    def test_review_task_routes_to_reviews(self):
        with tempfile.TemporaryDirectory() as tmp:
            case_dir = Path(tmp) / "C01_Test"
            task_path = case_dir / "tasks" / "T003.md"
            task_path.parent.mkdir(parents=True)
            metadata = {
                "task_id": "T003",
                "task_type": "REVIEW",
                "assignee_session": "Session-Review",
            }

            output = collab_watch.output_path_for_task(task_path, metadata)

        self.assertEqual(output, case_dir / "reviews" / "REVIEW_T003.md")

    def test_seen_state_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "runtime" / "Session-A.json"
            collab_watch.save_seen(state, {"a.md", "b.md"})
            loaded = collab_watch.load_seen(state)

        self.assertEqual(loaded, {"a.md", "b.md"})


if __name__ == "__main__":
    unittest.main()
