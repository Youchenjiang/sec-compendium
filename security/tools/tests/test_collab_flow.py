import argparse
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
import collab_watch


class CollabFlowIntegrationTests(unittest.TestCase):
    def test_dispatch_ack_question_reply_done_flow(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases = root / ".collab" / "cases"
            events = root / ".collab" / "runtime" / "events"
            case = cases / "C01_Test"
            for child in ("tasks", "findings", "reviews"):
                (case / child).mkdir(parents=True, exist_ok=True)
            (case / "CASE_STATE.md").write_text(
                "# State\n- **主導代理人 (Lead Session)**：`Session-Lead`\n",
                encoding="utf-8",
            )

            new_task = argparse.Namespace(
                case="C01_Test",
                actor_session="Session-Lead",
                task_id="T001",
                task_type="TRIAGE",
                target_role="ROLE_01_TRIAGE_HUNTER",
                assignee_session="Session-Worker",
                question="Q02",
                title="Find suspicious process",
                objective="Identify the suspicious process from supplied evidence.",
                context="Synthetic integration-test context only.",
                skills="memory triage",
            )
            state_path = root / ".collab" / "runtime" / "watchers" / "Session-Worker.json"
            state = {"seen_tasks": set(), "seen_events": set()}

            with (
                patch.object(protocol, "REPO_ROOT", root),
                patch.object(protocol, "CASES_DIR", cases),
                patch.object(protocol, "EVENTS_DIR", events),
                patch.object(collab_watch, "CASES_DIR", cases),
                patch.object(collab_watch, "copy_to_clipboard"),
                patch.object(collab_watch, "beep"),
            ):
                self.assertEqual(collab_bus.command_new_task(new_task), 0)
                task_path, metadata = protocol.find_task("C01_Test", "T001")
                self.assertEqual(metadata["assignee_session"], "Session-Worker")

                announced = collab_watch.process_assignments(
                    session="Session-Worker",
                    case_filters={"C01_Test"},
                    state=state,
                    state_path=state_path,
                    exec_program=None,
                    exec_args=[],
                )
                self.assertEqual(announced, 1)

                start_args = argparse.Namespace(
                    case="C01_Test",
                    task_id="T001",
                    session="Session-Worker",
                    message="Starting triage",
                )
                self.assertEqual(collab_bus.emit_worker_event(start_args, "START"), 0)

                question_args = argparse.Namespace(
                    case="C01_Test",
                    task_id="T001",
                    from_session="Session-Worker",
                    to_session="Session-Lead",
                    kind="QUESTION",
                    message="Use UTC?",
                )
                self.assertEqual(collab_bus.command_send(question_args), 0)

                reply_args = argparse.Namespace(
                    case="C01_Test",
                    task_id="T001",
                    from_session="Session-Lead",
                    to_session="Session-Worker",
                    kind="REPLY",
                    message="Yes, use UTC.",
                )
                self.assertEqual(collab_bus.command_send(reply_args), 0)

                init_args = argparse.Namespace(
                    case="C01_Test", task_id="T001", session="Session-Worker"
                )
                self.assertEqual(collab_bus.command_init_output(init_args), 0)
                output_path = protocol.output_path_for_task(task_path, metadata)
                self.assertTrue(output_path.exists())
                output_text = output_path.read_text(encoding="utf-8")
                output_text = output_text.replace("`TODO`", "`HIGH`", 1)
                output_text = output_text.replace(
                    "- **Answer / Conclusion**：TODO",
                    "- **Answer / Conclusion**：PID 4242 synthetic-process.exe",
                )
                output_text = output_text.replace(
                    "- **Artifact / Source**：TODO",
                    "- **Artifact / Source**：synthetic-memory.raw",
                )
                output_text = output_text.replace(
                    "- **取得方法 / Tool**：TODO",
                    "- **取得方法 / Tool**：integration-test parser",
                )
                output_text = output_text.replace(
                    "- **Direct Observation**：TODO",
                    "- **Direct Observation**：PID 4242 is present in the synthetic fixture",
                )
                output_text = output_text.replace(
                    "- **Reproduction**：TODO",
                    "- **Reproduction**：run the integration fixture parser once",
                )
                output_text = output_text.replace(
                    "- **Known Limitations**：TODO",
                    "- **Known Limitations**：synthetic protocol test only",
                )
                output_text = output_text.replace(
                    "- **建議答案狀態**：`TODO`",
                    "- **建議答案狀態**：`VERIFIED`",
                )
                output_text = output_text.replace(
                    "- **需要額外 review**：`TODO`",
                    "- **需要額外 review**：`NO`",
                )
                output_path.write_text(output_text, encoding="utf-8")

                done_args = argparse.Namespace(
                    case="C01_Test",
                    task_id="T001",
                    session="Session-Worker",
                    message="Finding ready for review",
                )
                self.assertEqual(collab_bus.emit_worker_event(done_args, "DONE"), 0)
                self.assertEqual(protocol.latest_task_state("C01_Test", "T001"), "DONE")

                kinds_to_lead = [
                    payload["kind"]
                    for _, payload in protocol.incoming_events("Session-Lead")
                ]
                self.assertEqual(
                    kinds_to_lead,
                    ["ACK", "START", "QUESTION", "DONE"],
                )
                kinds_to_worker = [
                    payload["kind"]
                    for _, payload in protocol.incoming_events("Session-Worker")
                ]
                self.assertEqual(kinds_to_worker, ["DISPATCHED", "REPLY"])


if __name__ == "__main__":
    unittest.main()
