"""
Unit tests for Scanner and vulnerability detection rules.
"""
import unittest
import tempfile
import shutil
from pathlib import Path

from security.tools.code_auditor.core.scanner import Scanner


class TestScanner(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.scanner = Scanner(deep=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_detect_direct_eval_sink(self):
        test_file = Path(self.temp_dir) / "eval_test.php"
        test_file.write_text("<?php\neval($_GET['payload']);\n", encoding="utf-8")

        findings = self.scanner.scan_file(str(test_file))
        self.assertGreaterEqual(len(findings), 1)
        self.assertTrue(any("eval" in f.vuln_type.lower() or f.category == "code_execution" for f in findings))
        self.assertEqual(findings[0].severity, "CRITICAL")

    def test_detect_command_injection(self):
        test_file = Path(self.temp_dir) / "cmd_test.php"
        test_file.write_text("<?php\nsystem($_POST['target']);\n", encoding="utf-8")

        findings = self.scanner.scan_file(str(test_file))
        self.assertGreaterEqual(len(findings), 1)
        self.assertTrue(any("command" in f.vuln_type.lower() or "exec" in f.vuln_type.lower() for f in findings))

    def test_ignore_commented_code(self):
        test_file = Path(self.temp_dir) / "comment_test.php"
        test_file.write_text("<?php\n// system($_POST['target']);\n# eval($_GET['x']);\n", encoding="utf-8")

        findings = self.scanner.scan_file(str(test_file))
        self.assertEqual(len(findings), 0)

    def test_scan_directory(self):
        d = Path(self.temp_dir) / "src"
        d.mkdir()
        (d / "vuln.php").write_text("<?php\nunserialize($_COOKIE['data']);\n", encoding="utf-8")
        (d / "clean.php").write_text("<?php\necho 'hello world';\n", encoding="utf-8")

        findings = self.scanner.scan_directory(str(d))
        self.assertGreaterEqual(len(findings), 1)
        self.assertEqual(self.scanner.scanned_files, 2)


if __name__ == "__main__":
    unittest.main()
