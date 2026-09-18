"""
Unit tests for DockerTester sandbox verification.
"""
import unittest
import tempfile
import shutil
from security.tools.code_auditor.sandbox.docker_tester import create_tester


class TestDockerTester(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.tester = create_tester(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_missing_run_script_returns_three_tuple(self):
        # When run.sh does not exist, test_exploit should return a 3-tuple (bool, str, str)
        res = self.tester.test_exploit(
            exploit_path="dummy.py",
            php_version="8.4",
            package_name="test/pkg",
            package_version="1.0.0",
        )
        self.assertIsInstance(res, tuple)
        self.assertEqual(len(res), 3)
        success, output, analysis = res
        self.assertFalse(success)
        self.assertIn("run.sh not found", output)
        self.assertIn("Missing run.sh", analysis)


if __name__ == "__main__":
    unittest.main()
