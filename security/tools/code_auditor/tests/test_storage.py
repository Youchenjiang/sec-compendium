"""
Unit tests for Storage and Report Generation.
"""
import unittest
import tempfile
import shutil
from pathlib import Path

from security.tools.code_auditor.storage.recorder import Storage, RunRecord
from security.tools.code_auditor.core.types import Vulnerability


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.storage = Storage(base_dir=self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_exploit(self):
        p = self.storage.save_exploit("sample/pkg", "rce", "print('exploit')")
        self.assertTrue(p.exists())
        self.assertEqual(p.read_text(encoding="utf-8"), "print('exploit')")

    def test_save_vulnerability_report(self):
        vulns = [
            Vulnerability(
                vuln_type="Code Execution",
                file_path="src/index.php",
                line_number=1,
                code_snippet="eval($_GET['x']);",
                severity="CRITICAL",
                description="eval rce",
            )
        ]
        self.storage.save_vulnerability_report("sample/pkg", vulns)
        report_files = list((Path(self.temp_dir) / "reports").glob("*.json"))
        self.assertGreaterEqual(len(report_files), 1)

    def test_record_run_and_generate_writeup(self):
        record = RunRecord(
            timestamp="2026-09-18T00:00:00",
            package_name="sample/pkg",
            package_version="1.0.0",
            php_version="8.4",
            vulnerabilities=[
                {
                    "type": "Code Execution",
                    "file": "src/index.php",
                    "line": 1,
                    "code": "eval($_GET['x']);",
                    "severity": "CRITICAL",
                    "description": "eval rce",
                    "exploit_hint": "run cmd",
                }
            ],
            exploits_generated=["sample/pkg_rce.py"],
            exploit_results={},
            submission_result={"status": "success"},
        )
        self.storage.record_run(record)
        writeup_path = self.storage.generate_writeup(record)
        self.assertTrue(writeup_path.exists())
        content = writeup_path.read_text(encoding="utf-8")
        self.assertIn("sample/pkg", content)
        self.assertIn("Code Execution", content)
        self.assertIn("CRITICAL", content)


if __name__ == "__main__":
    unittest.main()
