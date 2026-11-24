"""Conservative final PR checks reject missing or unresolved findings."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pr_verification


class VerificationTests(unittest.TestCase):
    def test_quality_gate_status_decides_sonar_acceptance(self):
        pr = {"headRefOid": "a" * 40, "baseRefName": "main", "state": "OPEN",
              "statusCheckRollup": [{"name": name, "conclusion": "SUCCESS"}
                                    for name in pr_verification.REQUIRED]}
        # Duplication alone does not block: this repository defers to the gate itself.
        quality = {"metrics": {"new_duplicated_lines_density": "0.2"},
                   "quality_gate": {"status": "OK", "conditions": []}}
        report = {"counts": {"unresolved": 0}, "sonar": {"total": 0},
                  "sonar_quality": quality}
        result = pr_verification.summarize(pr, report, remote_sha="a" * 40)
        self.assertTrue(result["ready"])
        self.assertEqual(quality, result["sonar_quality"])
        quality["quality_gate"]["status"] = "ERROR"
        result = pr_verification.summarize(pr, report, remote_sha="a" * 40)
        self.assertFalse(result["ready"])
        self.assertIn("SonarQube quality gate not passed", result["problems"])
    def test_python_analyzer_is_required_only_when_python_changes(self):
        pr = {"headRefOid": "a" * 40, "baseRefName": "main", "state": "OPEN",
              "statusCheckRollup": [{"name": name, "conclusion": "SUCCESS"}
                                    for name in pr_verification.REQUIRED]}
        report = {"counts": {"unresolved": 0}, "sonar": {"total": 0}}
        pr["files"] = [{"path": "tracks/lab/notes.md"}]
        self.assertTrue(pr_verification.summarize(pr, report, remote_sha="a" * 40)["ready"])
        pr["files"] = [{"path": "security/tools/pr_tool.py"}]
        result = pr_verification.summarize(pr, report, remote_sha="a" * 40)
        self.assertFalse(result["ready"])
        self.assertTrue(any("Missing required check: DeepSource: Python" in error
                            for error in result["problems"]))
    def test_pending_skipped_and_findings_never_report_green(self):
        pr = {"headRefOid": "a" * 40, "baseRefName": "main",
              "statusCheckRollup": [{"name": "CI", "status": "IN_PROGRESS"},
                                    {"name": "Sourcery", "conclusion": "SKIPPED"}]}
        report = {"counts": {"unresolved": 1},
                  "sonar": {"total": 2, "issues": [{"key": "S1", "message": "msg", "component": "c.cs", "line": 1, "rule": "r1", "severity": "MAJOR"}]},
                  "threads": [{"id": "PRRT_1", "path": "file.cs", "line": 10, "resolved": False, "outdated": True}]}
        result = pr_verification.summarize(pr, report, remote_sha="a" * 40)
        self.assertFalse(result["ready"])
        self.assertEqual(["Sourcery"], result["skipped"])
        self.assertGreaterEqual(len(result["problems"]), 3)
        self.assertEqual([{"id": "PRRT_1", "path": "file.cs", "line": 10, "outdated": True}],
                         result["unresolved_thread_details"])
        self.assertEqual([{"key": "S1", "message": "msg", "component": "c.cs", "line": 1, "rule": "r1", "severity": "MAJOR"}],
                         result["sonar_issue_details"])

    def test_clean_snapshot_passes_with_explicit_skips(self):
        pr = {"headRefOid": "a" * 40, "baseRefName": "main", "state": "OPEN",
              "statusCheckRollup": [{"name": name, "conclusion": "SUCCESS"} for name in pr_verification.REQUIRED] + [
                                    {"name": "Sourcery", "conclusion": "SKIPPED"}]}
        report = {"counts": {"unresolved": 0}, "sonar": {"total": 0}}
        result = pr_verification.summarize(pr, report, remote_sha="a" * 40)
        self.assertTrue(result["ready"])
        self.assertEqual(["Sourcery"], result["skipped"])

    def test_verify_includes_live_check_status_urls_and_required_flags(self):
        pr = {"headRefOid": "a" * 40, "baseRefName": "main", "state": "OPEN",
              "statusCheckRollup": [{"name": name, "conclusion": "SUCCESS",
                                     "detailsUrl": "https://github.com/example/check"}
                                    for name in pr_verification.REQUIRED] + [
                                        {"context": "Sourcery review", "state": "PENDING",
                                         "targetUrl": "https://sourcery.ai"}]}
        report = {"counts": {"unresolved": 0}, "sonar": {"total": 0}}
        result = pr_verification.summarize(pr, report, remote_sha="a" * 40)
        self.assertFalse(result["ready"])
        self.assertEqual(len(pr_verification.REQUIRED) + 1, len(result["checks"]))
        self.assertEqual("https://github.com/example/check", result["checks"][0]["url"])
        self.assertTrue(result["checks"][0]["required"])
        self.assertFalse(result["checks"][-1]["required"])

    def test_required_checks_match_this_repository(self):
        for name in ("PR and commit policy", "Documentation & Playbooks Quality Audit",
                     "TruffleHog Secrets Scan", "SonarCloud", "SonarCloud Code Analysis",
                     "DeepSource: Secrets"):
            self.assertIn(name, pr_verification.REQUIRED)
        self.assertFalse(any("Clickra" in name or "NativeAOT" in name
                             for name in pr_verification.REQUIRED))
    def test_missing_playbook_audit_blocks_acceptance(self):
        pr = {"headRefOid": "a" * 40, "baseRefName": "main", "state": "OPEN",
              "statusCheckRollup": [{"name": name, "conclusion": "SUCCESS"}
                                    for name in pr_verification.REQUIRED
                                    if name != "Documentation & Playbooks Quality Audit"]}
        report = {"counts": {"unresolved": 0}, "sonar": {"total": 0}}
        result = pr_verification.summarize(pr, report, remote_sha="a" * 40)
        self.assertFalse(result["ready"])
        self.assertTrue(any("Documentation & Playbooks Quality Audit" in issue
                            for issue in result["problems"]))
    def test_merged_deleted_branch_reports_historical_checks(self):
        pr = {"headRefOid": "a" * 40, "baseRefName": "main", "state": "MERGED",
              "statusCheckRollup": [{"name": name, "conclusion": "SUCCESS"}
                                    for name in pr_verification.REQUIRED]}
        report = {"counts": {"unresolved": 0}, "sonar": {"total": 0}}
        result = pr_verification.summarize(pr, report, remote_sha=None)
        self.assertFalse(result["ready"])
        self.assertEqual("MERGED", result["state"])
        self.assertTrue(result["historical_checks_passed"])
        self.assertIn("PR is not open", result["problems"])

    def test_open_missing_remote_sha_remains_blocked(self):
        pr = {"headRefOid": "a" * 40, "baseRefName": "main", "state": "OPEN",
              "statusCheckRollup": [{"name": name, "conclusion": "SUCCESS"}
                                    for name in pr_verification.REQUIRED]}
        report = {"counts": {"unresolved": 0}, "sonar": {"total": 0}}
        result = pr_verification.summarize(pr, report, remote_sha=None)
        self.assertFalse(result["ready"])
        self.assertIn("PR HEAD differs from remote SHA", result["problems"])

    def test_merged_historical_checks_do_not_hide_failed_checks(self):
        pr = {"headRefOid": "a" * 40, "baseRefName": "main", "state": "MERGED",
              "statusCheckRollup": [{"name": name, "conclusion": "FAILURE" if name == "TruffleHog Secrets Scan" else "SUCCESS"}
                                    for name in pr_verification.REQUIRED]}
        report = {"counts": {"unresolved": 0}, "sonar": {"total": 0}}
        result = pr_verification.summarize(pr, report, remote_sha=None)
        self.assertFalse(result["historical_checks_passed"])
        self.assertTrue(any("TruffleHog Secrets Scan" in problem for problem in result["problems"]))

    def test_closed_unmerged_pr_not_ready(self):
        pr = {"headRefOid": "a" * 40, "baseRefName": "main", "state": "CLOSED",
              "statusCheckRollup": [{"name": name, "conclusion": "SUCCESS"}
                                    for name in pr_verification.REQUIRED]}
        report = {"counts": {"unresolved": 0}, "sonar": {"total": 0}}
        result = pr_verification.summarize(pr, report, remote_sha=None)
        self.assertFalse(result["ready"])
        self.assertFalse(result["historical_checks_passed"])
        self.assertIn("PR is not open", result["problems"])

    def test_missing_checks_fail_closed(self):
        with self.assertRaisesRegex(RuntimeError, "missing"):
            pr_verification.summarize({"headRefOid": "a" * 40},
                                      {"counts": {"unresolved": 0}, "sonar": {"total": 0}},
                                      remote_sha="a" * 40)

    def test_absent_provider_is_not_considered_passing(self):
        pr = {"headRefOid": "a" * 40, "baseRefName": "main", "state": "OPEN",
              "statusCheckRollup": [{"name": "CI", "conclusion": "SUCCESS"}]}
        result = pr_verification.summarize(
            pr, {"counts": {"unresolved": 0}, "sonar": {"total": 0}}, remote_sha="a" * 40)
        self.assertFalse(result["ready"])
        self.assertIn("Missing required check: TruffleHog Secrets Scan", result["problems"][-1])

    def test_skipped_required_provider_blocks_acceptance(self):
        pr = {"headRefOid": "a" * 40, "baseRefName": "main", "state": "OPEN",
              "statusCheckRollup": [{"name": name, "conclusion": "SKIPPED" if name == "DeepSource: Secrets" else "SUCCESS"}
                                    for name in pr_verification.REQUIRED]}
        report = {"counts": {"unresolved": 0}, "sonar": {"total": 0}}
        result = pr_verification.summarize(pr, report, remote_sha="a" * 40)
        self.assertFalse(result["ready"])
        self.assertTrue(any("required checks skipped" in issue for issue in result["problems"]))

    def test_top_level_review_finding_blocks_acceptance(self):
        pr = {"headRefOid": "a" * 40, "baseRefName": "main", "state": "OPEN",
              "statusCheckRollup": [{"name": name, "conclusion": "SUCCESS"}
                                    for name in pr_verification.REQUIRED]}
        report = {
            "counts": {"unresolved": 0},
            "sonar": {"total": 0},
            "reviews": [{
                "author": "llamapreview",
                "state": "COMMENTED",
                "body": "### LlamaPReview — Blocking issues found\n\nSome issue details."
            }]
        }
        result = pr_verification.summarize(pr, report, remote_sha="a" * 40)
        self.assertFalse(result["ready"])
        self.assertTrue(any("unaddressed top-level review finding" in issue for issue in result["problems"]))
        self.assertEqual(1, len(result["top_level_findings"]))
        self.assertEqual("llamapreview", result["top_level_findings"][0]["author"])
        self.assertFalse(result["top_level_findings"][0]["addressed"])

    def test_addressed_top_level_review_finding_allows_acceptance(self):
        pr = {"headRefOid": "a" * 40, "baseRefName": "main", "state": "OPEN",
              "body": "## Review Follow-ups\n- @llamapreview: Addressed in commit b1fa2031",
              "statusCheckRollup": [{"name": name, "conclusion": "SUCCESS"}
                                    for name in pr_verification.REQUIRED]}
        report = {
            "counts": {"unresolved": 0},
            "sonar": {"total": 0},
            "reviews": [{
                "author": "llamapreview",
                "relation": "historical",
                "state": "COMMENTED",
                "body": "### LlamaPReview — Blocking issues found\n\nSome issue details."
            }]
        }
        result = pr_verification.summarize(pr, report, remote_sha="a" * 40)
        self.assertTrue(result["ready"])
        self.assertEqual(1, len(result["top_level_findings"]))
        self.assertTrue(result["top_level_findings"][0]["addressed"])


    def test_clean_review_notice_is_not_treated_as_finding(self):
        pr = {"headRefOid": "a" * 40, "baseRefName": "main", "state": "OPEN",
              "statusCheckRollup": [{"name": name, "conclusion": "SUCCESS"}
                                    for name in pr_verification.REQUIRED]}
        report = {
            "counts": {"unresolved": 0},
            "sonar": {"total": 0},
            "reviews": [{
                "author": "llamapreview",
                "state": "COMMENTED",
                "body": "### LlamaPReview — No blocking issues found\n\nThe strategy resolver preserves Windows conversion."
            }]
        }
        result = pr_verification.summarize(pr, report, remote_sha="a" * 40)
        self.assertTrue(result["ready"])
        self.assertEqual(0, len(result["top_level_findings"]))

    def test_mixed_review_with_clean_phrase_and_action_required_is_detected(self):
        pr = {"headRefOid": "a" * 40, "baseRefName": "main", "state": "OPEN",
              "statusCheckRollup": [{"name": name, "conclusion": "SUCCESS"}
                                    for name in pr_verification.REQUIRED]}
        report = {
            "counts": {"unresolved": 0},
            "sonar": {"total": 0},
            "reviews": [{
                "author": "llamapreview",
                "state": "COMMENTED",
                "body": "### LlamaPReview — No blocking issues found in module A\n\nAction required: please fix buffer handling."
            }]
        }
        result = pr_verification.summarize(pr, report, remote_sha="a" * 40)
        self.assertFalse(result["ready"])
        self.assertEqual(1, len(result["top_level_findings"]))
        self.assertTrue(any("1 unaddressed top-level review finding(s)" in p for p in result["problems"]))


if __name__ == "__main__":
    unittest.main()
