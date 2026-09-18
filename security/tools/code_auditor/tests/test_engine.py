"""
Integration tests for CodeAuditor core engine.
"""
import unittest
import tempfile
import shutil
from pathlib import Path

from security.tools.code_auditor.engine import CodeAuditor
from security.tools.code_auditor.storage.recorder import Storage


class TestCodeAuditorEngine(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.results_dir = tempfile.mkdtemp()

        # Create a mock PHP project
        src_dir = Path(self.temp_dir) / "src"
        src_dir.mkdir()
        (src_dir / "index.php").write_text("<?php\necho 'hello';\n", encoding="utf-8")
        (src_dir / "vuln.php").write_text("<?php\neval($_GET['code']);\n", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        shutil.rmtree(self.results_dir, ignore_errors=True)

    def test_audit_directory_scan_only(self):
        storage = Storage(base_dir=self.results_dir)
        auditor = CodeAuditor(storage=storage)
        auditor.audit_directory(self.temp_dir, scan_only=True)

        self.assertEqual(auditor.stats["targets_scanned"], 1)
        self.assertTrue(auditor.stats["vulnerabilities_found"] >= 1)
        self.assertEqual(auditor.stats["exploits_generated"], 0)


if __name__ == "__main__":
    unittest.main()
