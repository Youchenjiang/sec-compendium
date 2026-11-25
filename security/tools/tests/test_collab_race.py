import argparse
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import collab_protocol as protocol
import collab_race
import collab_watch


class CollabRaceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.cases = self.root / ".collab" / "cases"
        self.events = self.root / ".collab" / "runtime" / "events"
        self.inbox = self.root / ".collab" / "runtime" / "inbox"
        self.race = self.root / ".collab" / "runtime" / "race"
        self.case = self.cases / "C01_Test"
        for child in ("tasks", "findings", "reviews"):
            (self.case / child).mkdir(parents=True, exist_ok=True)
        (self.case / "CASE_STATE.md").write_text(
            "# State\n- **銝餃?隞??鈭?(Lead Session)**嚗Session-Lead`\n",
            encoding="utf-8",
        )
        self.patches = [
            patch.object(protocol, "REPO_ROOT", self.root),
            patch.object(protocol, "CASES_DIR", self.cases),
            patch.object(protocol, "EVENTS_DIR", self.events),
            patch.object(protocol, "INBOX_DIR", self.inbox),
            patch.object(protocol, "get_case_lead", return_value="Session-Lead"),
            patch.object(collab_race.collab_bus, "ensure_actor_is_case_lead", return_value="Session-Lead"),
            patch.object(collab_race, "RACE_DIR", self.race),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in reversed(self.patches):
            p.stop()
        self.tmp.cleanup()

    def open_race(self):
        return collab_race.command_open(argparse.Namespace(
            case="C01_Test", lead_session="Session-Lead", budget_minutes=30, target_ready_ratio=0.8
        ))

    def lane(self, task_id="T001", lane_id="L01", assignee="Session-A", questions="Q01,Q02"):
        return collab_race.command_lane(argparse.Namespace(
            case="C01_Test", lead_session="Session-Lead", lane_id=lane_id,
            task_id=task_id, task_type="TRIAGE", target_role="ROLE_01_TRIAGE_HUNTER",
            assignee_session=assignee, execution_environment="portable_text_any",
            questions=questions, domain="execution", objective="Resolve assigned questions",
            context="fixture", skills="triage",
        ))

    def answer(self, task_id, session, question, answer, evidence, **kw):
        args = dict(
            case="C01_Test", task_id=task_id, session=session, question=question,
            answer=answer, confidence="high", evidence=evidence, state="auto",
            semantic_risk=False, needs_review=False, secret_ref="",
            secret_sha256="", secret_exact=False,
        )
        args.update(kw)
        return collab_race.command_answer(argparse.Namespace(**args))

    def secret_answer(self, task_id, session, question, evidence, **kw):
        args = dict(
            case="C01_Test", task_id=task_id, session=session, question=question,
            answer="", confidence="high", evidence=evidence, state="auto",
            semantic_risk=False, needs_review=False,
            secret_ref=r"%TEMP%\fixture.secret",
            secret_sha256="a" * 64,
            secret_exact=True,
        )
        args.update(kw)
        return collab_race.command_answer(argparse.Namespace(**args))

    def test_lane_is_multi_question_governed_task(self):
        self.assertEqual(self.open_race(), 0)
        self.assertEqual(self.lane(), 0)
        task_path, metadata = protocol.find_task("C01_Test", "T001")
        self.assertEqual(metadata["questions"], "Q01, Q02")
        self.assertEqual(metadata["execution_profile"], "race")
        self.assertEqual(metadata["lane_id"], "L01")
        self.assertEqual(protocol.latest_task_state("C01_Test", "T001"), "DISPATCHED")
        lanes = [p for _, p in collab_race.iter_race_events("C01_Test") if p["kind"] == "LANE_DISPATCHED"]
        self.assertEqual(lanes[0]["data"]["questions"], ["Q01", "Q02"])
        self.assertEqual(lanes[0]["data"]["task_sha256"], protocol.sha256_file(task_path))

    def test_ready_answer_can_publish_before_ack_start_done(self):
        self.open_race(); self.lane()
        self.assertEqual(self.answer("T001", "Session-A", "Q01", "10.0.0.5", ["evtx:4624", "mft:123"]), 0)
        self.assertEqual(protocol.latest_task_state("C01_Test", "T001"), "DISPATCHED")
        board = collab_race.build_board("C01_Test")
        self.assertEqual(board["Q01"]["state"], "READY")
        self.assertEqual(board["Q01"]["answer"], "10.0.0.5")

    def test_semantic_risk_forces_candidate(self):
        self.open_race(); self.lane()
        self.answer("T001", "Session-A", "Q01", "MEGA used", ["prefetch", "userassist"], semantic_risk=True)
        board = collab_race.build_board("C01_Test")
        self.assertEqual(board["Q01"]["state"], "CANDIDATE")
        self.assertTrue(board["Q01"]["needs_review"])

    def test_conflicting_lanes_are_detected_without_shared_board_writes(self):
        self.open_race(); self.lane("T001", "L01", "Session-A", "Q01")
        self.lane("T002", "L02", "Session-B", "Q01")
        self.answer("T001", "Session-A", "Q01", "alpha", ["a1", "a2"])
        self.answer("T002", "Session-B", "Q01", "beta", ["b1", "b2"])
        board = collab_race.build_board("C01_Test")
        self.assertEqual(board["Q01"]["state"], "CONFLICT")
        self.assertTrue(board["Q01"]["needs_review"])
        self.assertEqual(board["Q01"]["candidate_count"], 2)

    def test_only_ready_answer_can_be_submitted(self):
        self.open_race(); self.lane()
        self.answer("T001", "Session-A", "Q01", "alpha", ["a1"], confidence="medium")
        with self.assertRaisesRegex(ValueError, "only READY"):
            collab_race.command_control(argparse.Namespace(
                case="C01_Test", lead_session="Session-Lead", question="Q01", answer="", note=""
            ), "SUBMITTED")
        self.answer("T001", "Session-A", "Q01", "alpha", ["a1", "a2"])
        self.assertEqual(collab_race.command_control(argparse.Namespace(
            case="C01_Test", lead_session="Session-Lead", question="Q01", answer="", note=""
        ), "SUBMITTED"), 0)
        self.assertEqual(collab_race.build_board("C01_Test")["Q01"]["state"], "SUBMITTED")

    def test_metrics_track_answer_readiness_not_task_done(self):
        self.open_race(); self.lane()
        self.answer("T001", "Session-A", "Q01", "alpha", ["a1", "a2"])
        metrics = collab_race.race_metrics("C01_Test")
        self.assertEqual(metrics["question_count"], 2)
        self.assertEqual(metrics["ready_count"], 1)
        self.assertAlmostEqual(metrics["ready_ratio"], 0.5)
        self.assertIsNotNone(metrics["first_lane_seconds"])
        self.assertIsNotNone(metrics["first_ready_seconds"])


    def test_race_doctor_validates_hash_anchored_lane_and_answer(self):
        self.open_race(); self.lane()
        self.answer("T001", "Session-A", "Q01", "alpha", ["a1", "a2"])
        self.assertEqual(collab_race.validate_race_case("C01_Test"), [])

    def test_submit_accept_state_machine_locks_answer(self):
        self.open_race(); self.lane()
        self.answer("T001", "Session-A", "Q01", "alpha", ["a1", "a2"])
        ctl = argparse.Namespace(case="C01_Test", lead_session="Session-Lead", question="Q01", answer="", note="")
        self.assertEqual(collab_race.command_control(ctl, "SUBMITTED"), 0)
        with self.assertRaisesRegex(ValueError, "locked"):
            self.answer("T001", "Session-A", "Q01", "beta", ["b1", "b2"])
        self.assertEqual(collab_race.command_control(ctl, "ACCEPTED"), 0)
        self.assertEqual(collab_race.build_board("C01_Test")["Q01"]["state"], "ACCEPTED")

    def test_rejected_answer_can_be_reopened_by_new_evidence(self):
        self.open_race(); self.lane()
        self.answer("T001", "Session-A", "Q01", "alpha", ["a1", "a2"])
        ctl = argparse.Namespace(case="C01_Test", lead_session="Session-Lead", question="Q01", answer="", note="")
        collab_race.command_control(ctl, "SUBMITTED")
        collab_race.command_control(ctl, "REJECTED")
        self.answer("T001", "Session-A", "Q01", "beta", ["b1", "b2"])
        row = collab_race.build_board("C01_Test")["Q01"]
        self.assertEqual(row["state"], "READY")
        self.assertEqual(row["answer"], "beta")

    def test_closed_race_remains_inspectable_and_metrics_freeze(self):
        self.open_race(); self.lane()
        self.answer("T001", "Session-A", "Q01", "alpha", ["a1", "a2"])
        close = argparse.Namespace(case="C01_Test", lead_session="Session-Lead", note="fixture done")
        self.assertEqual(collab_race.command_close(close), 0)
        first = collab_race.race_metrics("C01_Test")
        second = collab_race.race_metrics("C01_Test")
        self.assertTrue(first["closed"])
        self.assertEqual(first["elapsed_seconds"], second["elapsed_seconds"])
        self.assertEqual(collab_race.command_board(argparse.Namespace(case="C01_Test")), 0)

    def test_answer_after_close_is_rejected_without_new_race_event(self):
        self.open_race(); self.lane()
        close = argparse.Namespace(case="C01_Test", lead_session="Session-Lead", note="fixture done")
        self.assertEqual(collab_race.command_close(close), 0)
        before = len(collab_race.iter_race_events("C01_Test"))
        with self.assertRaisesRegex(ValueError, "already closed"):
            self.answer("T001", "Session-A", "Q01", "late", ["a1", "a2"])
        after = len(collab_race.iter_race_events("C01_Test"))
        self.assertEqual(after, before)

    def test_secret_answer_can_be_ready_without_plaintext_persistence(self):
        self.open_race(); self.lane()
        self.assertEqual(
            self.secret_answer("T001", "Session-A", "Q01", ["registry:token", "registry-log:token"]),
            0,
        )
        row = collab_race.build_board("C01_Test")["Q01"]
        self.assertEqual(row["state"], "READY")
        self.assertEqual(row["answer"], r"[REDACTED: host-local %TEMP%\fixture.secret]")
        self.assertEqual(row["candidates"][0]["secret_sha256"], "a" * 64)
        self.assertTrue(row["candidates"][0]["secret_exact"])
        event_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path, payload in collab_race.iter_race_events("C01_Test")
            if payload["kind"] == "ANSWER_READY"
        )
        self.assertNotIn("plaintext-secret-value", event_text)
        self.assertNotIn('"secret_value"', event_text)

    def test_duplicate_identical_ready_publish_is_idempotent(self):
        self.open_race(); self.lane()
        self.answer("T001", "Session-A", "Q01", "alpha", ["a1", "a2"])
        self.answer("T001", "Session-A", "Q01", "alpha", ["a2", "a1"])
        ready_events = [
            payload
            for _, payload in collab_race.iter_race_events("C01_Test")
            if payload["kind"] == "ANSWER_READY"
        ]
        self.assertEqual(len(ready_events), 1)

    def test_board_can_reconstruct_state_at_elapsed_cutoff(self):
        t0 = 1_000_000_000_000
        with patch.object(collab_race.time, "time_ns", return_value=t0):
            self.open_race()
        with patch.object(collab_race.time, "time_ns", return_value=t0 + 1_000_000_000):
            self.lane()
        with patch.object(collab_race.time, "time_ns", return_value=t0 + 5 * 60 * 1_000_000_000):
            self.answer(
                "T001", "Session-A", "Q01", "alpha", ["a1"],
                confidence="medium",
            )
        with patch.object(collab_race.time, "time_ns", return_value=t0 + 20 * 60 * 1_000_000_000):
            self.answer("T001", "Session-A", "Q01", "alpha", ["a1", "a2"])

        at_15 = collab_race.build_board(
            "C01_Test", at_ns=t0 + 15 * 60 * 1_000_000_000
        )
        at_30 = collab_race.build_board(
            "C01_Test", at_ns=t0 + 30 * 60 * 1_000_000_000
        )
        self.assertEqual(at_15["Q01"]["state"], "CANDIDATE")
        self.assertEqual(at_30["Q01"]["state"], "READY")
        metrics = collab_race.race_metrics("C01_Test")
        self.assertEqual(metrics["ready_ratio_at_15m"], 0.0)
        self.assertEqual(metrics["ready_ratio_at_30m"], 0.5)

    def test_lead_answer_requires_explicit_lane_assist_event(self):
        self.open_race(); self.lane()
        with self.assertRaisesRegex(ValueError, "assist"):
            self.answer("T001", "Session-Lead", "Q01", "alpha", ["a1", "a2"])
        assist = argparse.Namespace(
            case="C01_Test", lead_session="Session-Lead", task_id="T001",
            reason="worker startup exceeded SLO",
        )
        self.assertEqual(collab_race.command_assist(assist), 0)
        self.assertEqual(
            self.answer("T001", "Session-Lead", "Q01", "alpha", ["a1", "a2"]),
            0,
        )
        row = collab_race.build_board("C01_Test")["Q01"]
        self.assertEqual(row["state"], "READY")
        self.assertEqual(row["candidates"][0]["actor_session"], "Session-Lead")
        assist_events = [
            payload for _, payload in collab_race.iter_race_events("C01_Test")
            if payload["kind"] == "LANE_ASSISTED"
        ]
        self.assertEqual(len(assist_events), 1)
        self.assertEqual(assist_events[0]["data"]["task_id"], "T001")
        answer_event = next(
            payload for _, payload in collab_race.iter_race_events("C01_Test")
            if payload["kind"] == "ANSWER_READY"
        )
        self.assertEqual(
            answer_event["data"]["assist_event_id"],
            assist_events[0]["event_id"],
        )

    def test_doctor_rejects_lead_answer_if_assist_only_happens_after_answer(self):
        self.open_race(); self.lane()
        task_path, _ = protocol.find_task("C01_Test", "T001")
        t0 = max(
            int(payload["created_ns"])
            for _, payload in collab_race.iter_race_events("C01_Test")
        ) + 1
        with patch.object(collab_race.time, "time_ns", return_value=t0):
            collab_race._write_event(
                kind="ANSWER_READY",
                case_id="C01_Test",
                actor_session="Session-Lead",
                data={
                    "lane_id": "L01",
                    "task_id": "T001",
                    "task_sha256": protocol.sha256_file(task_path),
                    "question_id": "Q01",
                    "answer": "alpha",
                    "confidence": "high",
                    "evidence": ["a1", "a2"],
                    "semantic_risk": False,
                    "needs_review": False,
                },
            )
        with patch.object(collab_race.time, "time_ns", return_value=t0 + 1):
            collab_race.command_assist(argparse.Namespace(
                case="C01_Test", lead_session="Session-Lead",
                task_id="T001", reason="too late",
            ))
        errors = collab_race.validate_race_case("C01_Test")
        self.assertTrue(any("assist" in error and "predate" in error for error in errors))

    def test_lead_owned_lane_auto_ack_starts_without_manual_bootstrap(self):
        self.open_race()
        self.lane(assignee="Session-Lead")
        self.assertEqual(protocol.latest_task_state("C01_Test", "T001"), "START")
        kinds = [
            payload["kind"]
            for _, payload in protocol.events_for_task("C01_Test", "T001")
        ]
        self.assertIn("ACK", kinds)
        self.assertIn("START", kinds)

    def test_metrics_report_milestones_and_do_not_predict_future_cutoffs(self):
        t0 = 4_000_000_000_000
        with patch.object(collab_race.time, "time_ns", return_value=t0):
            self.open_race()
        with patch.object(collab_race.time, "time_ns", return_value=t0 + 1_000_000_000):
            self.lane()
        with patch.object(collab_race.time, "time_ns", return_value=t0 + 10 * 60 * 1_000_000_000):
            self.answer("T001", "Session-A", "Q01", "alpha", ["a1", "a2"])
        with patch.object(collab_race.time, "time_ns", return_value=t0 + 12 * 60 * 1_000_000_000):
            self.answer("T001", "Session-A", "Q02", "beta", ["b1", "b2"])
        with patch.object(collab_race.time, "time_ns", return_value=t0 + 12 * 60 * 1_000_000_000):
            metrics = collab_race.race_metrics("C01_Test")
        self.assertEqual(metrics["ready_50_seconds"], 600.0)
        self.assertEqual(metrics["ready_80_seconds"], 720.0)
        self.assertEqual(metrics["ready_100_seconds"], 720.0)
        self.assertIsNone(metrics["ready_ratio_at_15m"])
        self.assertIsNone(metrics["ready_ratio_at_30m"])

        with patch.object(collab_race.time, "time_ns", return_value=t0 + 13 * 60 * 1_000_000_000):
            self.assertEqual(
                collab_race.command_close(argparse.Namespace(
                    case="C01_Test", lead_session="Session-Lead", note="fixture done"
                )),
                0,
            )
        metrics = collab_race.race_metrics("C01_Test")
        self.assertEqual(metrics["ready_ratio_at_15m"], 1.0)
        self.assertEqual(metrics["ready_ratio_at_30m"], 1.0)

    def test_watchdog_marks_unstarted_lane_overdue_and_can_enable_assist(self):
        t0 = 2_000_000_000_000
        with patch.object(collab_race.time, "time_ns", return_value=t0):
            self.open_race()
        with patch.object(collab_race.time, "time_ns", return_value=t0 + 1_000_000_000):
            self.lane()
        rows = collab_race.race_watchdog(
            "C01_Test",
            start_slo_seconds=60,
            now_ns=t0 + 70 * 1_000_000_000,
        )
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0]["overdue"])
        self.assertFalse(rows[0]["started"])
        with patch.object(collab_race.time, "time_ns", return_value=t0 + 70 * 1_000_000_000):
            rc = collab_race.command_watchdog(argparse.Namespace(
                case="C01_Test", lead_session="Session-Lead",
                start_slo_seconds=60, assist_overdue=True,
            ))
        self.assertEqual(rc, 0)
        self.assertTrue(collab_race._lane_has_assist("C01_Test", "T001"))

    def test_open_can_require_successful_dfir_preflight(self):
        required = argparse.Namespace(
            case="C01_Test", lead_session="Session-Lead", budget_minutes=30,
            target_ready_ratio=0.8, worker_start_slo_seconds=60,
            require_dfir_preflight=True,
        )
        with self.assertRaisesRegex(ValueError, "DFIR preflight"):
            collab_race.command_open(required)
        collab_race._write_event(
            kind="PREFLIGHT_PASSED",
            case_id="C01_Test",
            actor_session="Session-Lead",
            data={"ready": True, "capabilities": {"ntfs": True}},
        )
        self.assertEqual(collab_race.command_open(required), 0)

    def test_failed_preflight_does_not_satisfy_open_gate(self):
        collab_race._write_event(
            kind="PREFLIGHT_FAILED",
            case_id="C01_Test",
            actor_session="Session-Lead",
            data={"ready": False, "errors": ["fixture"]},
        )
        required = argparse.Namespace(
            case="C01_Test", lead_session="Session-Lead", budget_minutes=30,
            target_ready_ratio=0.8, worker_start_slo_seconds=60,
            require_dfir_preflight=True,
        )
        with self.assertRaisesRegex(ValueError, "DFIR preflight"):
            collab_race.command_open(required)


    def test_race_lane_handoff_instruction_streams_answers_before_done(self):
        self.open_race(); self.lane()
        task_path, metadata = protocol.find_task("C01_Test", "T001")
        output_path = protocol.output_path_for_task(task_path, metadata)
        instruction = collab_watch.build_task_instruction("Session-A", task_path, output_path, metadata)
        self.assertIn("RACE MODE lane=L01", instruction)
        self.assertIn("collab_race.py answer", instruction)
        self.assertIn("do not wait for task DONE", instruction)


    def test_explicit_ready_cannot_bypass_evidence_gate(self):
        self.open_race(); self.lane()
        with self.assertRaisesRegex(ValueError, "READY requires"):
            self.answer("T001", "Session-A", "Q01", "alpha", ["a1"], state="ready")
        with self.assertRaisesRegex(ValueError, "READY requires"):
            self.answer("T001", "Session-A", "Q01", "alpha", ["a1", "a1"], state="ready")
        with self.assertRaisesRegex(ValueError, "READY requires"):
            self.answer("T001", "Session-A", "Q01", "alpha", ["a1", "a2"], state="ready", confidence="medium")

    def test_control_event_cannot_replace_validated_answer(self):
        self.open_race(); self.lane()
        self.answer("T001", "Session-A", "Q01", "alpha", ["a1", "a2"])
        bad = argparse.Namespace(case="C01_Test", lead_session="Session-Lead", question="Q01", answer="beta", note="")
        with self.assertRaisesRegex(ValueError, "cannot replace"):
            collab_race.command_control(bad, "SUBMITTED")
        good = argparse.Namespace(case="C01_Test", lead_session="Session-Lead", question="Q01", answer="alpha", note="")
        collab_race.command_control(good, "SUBMITTED")
        with self.assertRaisesRegex(ValueError, "cannot replace"):
            collab_race.command_control(bad, "ACCEPTED")

    def test_dispatch_failed_lane_cannot_publish_answer(self):
        self.open_race(); self.lane()
        collab_race.collab_bus.command_dispatch_failed(argparse.Namespace(
            case="C01_Test", task_id="T001", session="Session-Lead", message="fixture dispatch failure"
        ))
        with self.assertRaisesRegex(ValueError, "failed task state"):
            self.answer("T001", "Session-A", "Q01", "alpha", ["a1", "a2"])


if __name__ == "__main__":
    unittest.main()
