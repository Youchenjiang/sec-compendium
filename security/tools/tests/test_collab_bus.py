import argparse
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import collab_bus
import collab_protocol as protocol


TASK_BODY = """# TASK: test

- **所屬大題**：`C01_Test`
- **關聯小題**：`Q02`
- **任務類型**：`TRIAGE`
- **Protocol Contract**：`v2.3`
- **Target Role**：`ROLE_01_TRIAGE_HUNTER`
- **Assignee Session**：`Session-Worker`
- **發起 Session**：`Session-Lead`
- **Execution Environment**：`portable_text_any`
- **Task ID**：`T001`
"""


class CollabBusTests(unittest.TestCase):
    def build_case(self, root: Path) -> tuple[Path, Path]:
        cases = root / "cases"
        case = cases / "C01_Test"
        for child in ("tasks", "findings", "reviews"):
            (case / child).mkdir(parents=True, exist_ok=True)
        (case / "CASE_STATE.md").write_text(
            "# State\n- **主導代理人 (Lead Session)**：`Session-Lead`\n",
            encoding="utf-8",
        )
        task = case / "tasks" / "T001_TRIAGE.md"
        task.write_text(TASK_BODY, encoding="utf-8")
        return cases, task

    def test_wrong_assignee_cannot_emit_worker_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases, _ = self.build_case(Path(tmp))
            args = argparse.Namespace(
                case="C01_Test", task_id="T001", session="Session-Intruder", message=""
            )
            with patch.object(protocol, "CASES_DIR", cases):
                with self.assertRaisesRegex(ValueError, "不是 task assignee"):
                    collab_bus.emit_worker_event(args, "ACK")

    def test_done_requires_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases, _ = self.build_case(Path(tmp))
            args = argparse.Namespace(
                case="C01_Test", task_id="T001", session="Session-Worker", message=""
            )
            lifecycle = [
                (None, {"kind": "ACK", "from_session": "Session-Worker"}),
                (None, {"kind": "START", "from_session": "Session-Worker"}),
            ]
            with (
                patch.object(protocol, "CASES_DIR", cases),
                patch.object(protocol, "events_for_task", return_value=lifecycle),
            ):
                with self.assertRaisesRegex(ValueError, "governed output 必須存在"):
                    collab_bus.emit_worker_event(args, "DONE")

    def test_done_rejects_incomplete_output_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases, task = self.build_case(Path(tmp))
            output = cases / "C01_Test" / "findings" / "FINDING_T001.md"
            output.write_text("# FINDING\n", encoding="utf-8")
            args = argparse.Namespace(
                case="C01_Test", task_id="T001", session="Session-Worker", message=""
            )
            lifecycle = [
                (
                    None,
                    {
                        "kind": "DISPATCHED",
                        "from_session": "Session-Lead",
                        "task_sha256": protocol.sha256_file(task),
                    },
                ),
                (None, {"kind": "ACK", "from_session": "Session-Worker"}),
                (None, {"kind": "START", "from_session": "Session-Worker"}),
            ]
            with (
                patch.object(protocol, "CASES_DIR", cases),
                patch.object(protocol, "events_for_task", return_value=lifecycle),
            ):
                with self.assertRaisesRegex(ValueError, "output contract 未通過"):
                    collab_bus.emit_worker_event(args, "DONE")

    def test_start_requires_ack(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases, _ = self.build_case(Path(tmp))
            args = argparse.Namespace(
                case="C01_Test", task_id="T001", session="Session-Worker", message=""
            )
            with (
                patch.object(protocol, "CASES_DIR", cases),
                patch.object(protocol, "events_for_task", return_value=[]),
            ):
                with self.assertRaisesRegex(ValueError, "START 前.*ACK"):
                    collab_bus.emit_worker_event(args, "START")

    def test_done_requires_start(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases, _ = self.build_case(Path(tmp))
            args = argparse.Namespace(
                case="C01_Test", task_id="T001", session="Session-Worker", message=""
            )
            lifecycle = [(None, {"kind": "ACK", "from_session": "Session-Worker"})]
            with (
                patch.object(protocol, "CASES_DIR", cases),
                patch.object(protocol, "events_for_task", return_value=lifecycle),
            ):
                with self.assertRaisesRegex(ValueError, "DONE 前.*START"):
                    collab_bus.emit_worker_event(args, "DONE")

    def test_done_is_terminal_and_rejects_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases, task = self.build_case(root)
            events = root / ".collab" / "runtime" / "events"
            with (
                patch.object(protocol, "REPO_ROOT", root),
                patch.object(protocol, "CASES_DIR", cases),
                patch.object(protocol, "EVENTS_DIR", events),
            ):
                for kind in ("DISPATCHED", "ACK", "START", "DONE"):
                    protocol.emit_event(
                        kind=kind,
                        case_id="C01_Test",
                        task_id="T001",
                        from_session=("Session-Lead" if kind == "DISPATCHED" else "Session-Worker"),
                        to_session=("Session-Worker" if kind == "DISPATCHED" else "Session-Lead"),
                        task_path=task,
                    )
                args = argparse.Namespace(
                    case="C01_Test", task_id="T001", session="Session-Worker", message=""
                )
                with self.assertRaisesRegex(ValueError, "terminal state DONE"):
                    collab_bus.emit_worker_event(args, "START")
                with self.assertRaisesRegex(ValueError, "terminal state DONE"):
                    collab_bus.emit_worker_event(args, "ERROR")

    def test_send_rejects_nonparticipant(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases, _ = self.build_case(Path(tmp))
            args = argparse.Namespace(
                case="C01_Test",
                task_id="T001",
                from_session="Session-Intruder",
                to_session="Session-Lead",
                kind="NOTE",
                message="hello",
            )
            with patch.object(protocol, "CASES_DIR", cases):
                with self.assertRaisesRegex(ValueError, "只能在 Case Lead"):
                    collab_bus.command_send(args)

    def test_non_lead_cannot_create_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases, _ = self.build_case(Path(tmp))
            with patch.object(protocol, "CASES_DIR", cases):
                with self.assertRaisesRegex(ValueError, "不是 C01_Test 的 Case Lead"):
                    collab_bus.ensure_actor_is_case_lead("C01_Test", "Session-Intruder")

    def test_status_accepts_anchored_legacy_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases, task = self.build_case(root)
            events = root / "events"
            legacy_body = TASK_BODY.replace(
                "- **Protocol Contract**：`v2.3`\n", ""
            ).replace("- **Execution Environment**：`portable_text_any`\n", "")
            task.write_text(legacy_body, encoding="utf-8")
            output = cases / "C01_Test" / "findings" / "FINDING_T001.md"
            output.write_text("# historical finding\n", encoding="utf-8")
            with (
                patch.object(protocol, "REPO_ROOT", root),
                patch.object(protocol, "CASES_DIR", cases),
                patch.object(protocol, "EVENTS_DIR", events),
            ):
                protocol.emit_event(
                    kind="DISPATCHED",
                    case_id="C01_Test",
                    task_id="T001",
                    from_session="Session-Lead",
                    to_session="Session-Worker",
                    task_path=task,
                )
                buffer = io.StringIO()
                with contextlib.redirect_stdout(buffer):
                    self.assertEqual(
                        collab_bus.command_status(
                            argparse.Namespace(case="C01_Test", session=None)
                        ),
                        0,
                    )
            status_text = buffer.getvalue()
            self.assertIn("legacy DISPATCHED yes", status_text)
            self.assertNotIn("INVALID", status_text)

    def test_dispatch_failed_is_lead_only_and_pre_ack(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases, task = self.build_case(root)
            events = root / ".collab" / "runtime" / "events"
            with (
                patch.object(protocol, "REPO_ROOT", root),
                patch.object(protocol, "CASES_DIR", cases),
                patch.object(protocol, "EVENTS_DIR", events),
            ):
                protocol.emit_event(
                    kind="DISPATCHED",
                    case_id="C01_Test",
                    task_id="T001",
                    from_session="Session-Lead",
                    to_session="Session-Worker",
                    task_path=task,
                )
                intruder = argparse.Namespace(
                    case="C01_Test",
                    task_id="T001",
                    session="Session-Intruder",
                    message="bootstrap failed",
                )
                with self.assertRaisesRegex(ValueError, "不是 C01_Test 的 Case Lead"):
                    collab_bus.command_dispatch_failed(intruder)

                lead = argparse.Namespace(
                    case="C01_Test",
                    task_id="T001",
                    session="Session-Lead",
                    message="bootstrap failed",
                )
                self.assertEqual(collab_bus.command_dispatch_failed(lead), 0)
                self.assertEqual(
                    protocol.latest_task_state("C01_Test", "T001"),
                    "DISPATCH_FAILED",
                )

                protocol.emit_event(
                    kind="ACK",
                    case_id="C01_Test",
                    task_id="T001",
                    from_session="Session-Worker",
                    to_session="Session-Lead",
                    task_path=task,
                )
                with self.assertRaisesRegex(ValueError, "已有 ACK"):
                    collab_bus.command_dispatch_failed(
                        argparse.Namespace(
                            case="C01_Test",
                            task_id="T001",
                            session="Session-Lead",
                            message="late failure",
                        )
                    )

    def test_done_rejects_mutated_immutable_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases, task = self.build_case(root)
            events = root / ".collab" / "runtime" / "events"
            output = cases / "C01_Test" / "findings" / "FINDING_T001.md"
            output.write_text("# FINDING\n", encoding="utf-8")

            with (
                patch.object(protocol, "REPO_ROOT", root),
                patch.object(protocol, "CASES_DIR", cases),
                patch.object(protocol, "EVENTS_DIR", events),
            ):
                protocol.emit_event(
                    kind="DISPATCHED",
                    case_id="C01_Test",
                    task_id="T001",
                    from_session="Session-Lead",
                    to_session="Session-Worker",
                    task_path=task,
                )
                protocol.emit_event(
                    kind="ACK",
                    case_id="C01_Test",
                    task_id="T001",
                    from_session="Session-Worker",
                    to_session="Session-Lead",
                    task_path=task,
                )
                protocol.emit_event(
                    kind="START",
                    case_id="C01_Test",
                    task_id="T001",
                    from_session="Session-Worker",
                    to_session="Session-Lead",
                    task_path=task,
                )
                task.write_text(TASK_BODY + "\nmutated\n", encoding="utf-8")
                args = argparse.Namespace(
                    case="C01_Test",
                    task_id="T001",
                    session="Session-Worker",
                    message="",
                )
                with self.assertRaisesRegex(ValueError, "immutable task hash 已改變"):
                    collab_bus.emit_worker_event(args, "DONE")

    def test_review_task_requires_and_propagates_target_finding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases, _ = self.build_case(root)
            events = root / "events"
            finding = cases / "C01_Test" / "findings" / "FINDING_T001.md"
            finding.write_text("# FINDING: T001\n", encoding="utf-8")
            args = argparse.Namespace(
                case="C01_Test",
                actor_session="Session-Lead",
                task_id="T002",
                task_type="REVIEW",
                target_role="ROLE_03_DEVILS_ADVOCATE",
                assignee_session="Session-Reviewer",
                execution_environment="portable_text_any",
                review_target_finding="FINDING_T001",
                question="",
                title="Review T001",
                objective="Review the governed finding.",
                context="Synthetic review test only.",
                skills="independent review",
            )
            with (
                patch.object(protocol, "REPO_ROOT", root),
                patch.object(protocol, "CASES_DIR", cases),
                patch.object(protocol, "EVENTS_DIR", events),
            ):
                self.assertEqual(collab_bus.command_new_task(args), 0)
                task_path, metadata = protocol.find_task("C01_Test", "T002")
                self.assertEqual(metadata["review_target_finding"], "FINDING_T001")
                self.assertEqual(protocol.validate_task_metadata(task_path, metadata), [])
                init_args = argparse.Namespace(
                    case="C01_Test", task_id="T002", session="Session-Reviewer"
                )
                self.assertEqual(collab_bus.command_init_output(init_args), 0)
                review_path = cases / "C01_Test" / "reviews" / "REVIEW_T002.md"
                self.assertIn(
                    "- **對應 Finding**：`FINDING_T001`",
                    review_path.read_text(encoding="utf-8"),
                )

    def test_review_task_rejects_missing_target_finding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases, _ = self.build_case(root)
            args = argparse.Namespace(
                case="C01_Test",
                actor_session="Session-Lead",
                task_id="T002",
                task_type="REVIEW",
                target_role="ROLE_03_DEVILS_ADVOCATE",
                assignee_session="Session-Reviewer",
                execution_environment="portable_text_any",
                review_target_finding="",
                question="",
                title="Review T001",
                objective="Review the governed finding.",
                context="Synthetic review test only.",
                skills="independent review",
            )
            with patch.object(protocol, "CASES_DIR", cases):
                with self.assertRaisesRegex(ValueError, "review-target-finding"):
                    collab_bus.command_new_task(args)


if __name__ == "__main__":
    unittest.main()
