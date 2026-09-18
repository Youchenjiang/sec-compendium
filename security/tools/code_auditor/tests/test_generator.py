"""
Unit tests for ExploitGenerator.
"""
import unittest
from security.tools.code_auditor.generator.exploit_gen import create_generator
from security.tools.code_auditor.core.types import Vulnerability


class TestExploitGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = create_generator()
        self.target = {
            "name": "vendor/package",
            "version": "1.0.0",
            "php_version": "8.4",
        }

    def test_generate_file_put_contents_exploit(self):
        vuln = Vulnerability(
            vuln_type="file_put_contents with user input",
            file_path="src/uploader.php",
            line_number=42,
            code_snippet="file_put_contents($_GET['path'], $_GET['data']);",
            severity="HIGH",
            category="file_operation",
        )
        exploit = self.generator.generate_exploit(vuln, self.target)
        self.assertIsNotNone(exploit)
        self.assertIn("requests", exploit)
        self.assertIn("uploader.php", exploit)

    def test_generate_eval_exploit(self):
        vuln = Vulnerability(
            vuln_type="eval() with user input",
            file_path="admin/eval.php",
            line_number=10,
            code_snippet="eval($_GET['code']);",
            severity="CRITICAL",
            category="code_execution",
        )
        exploit = self.generator.generate_exploit(vuln, self.target)
        self.assertIsNotNone(exploit)
        self.assertIn("admin/eval.php", exploit)


if __name__ == "__main__":
    unittest.main()
