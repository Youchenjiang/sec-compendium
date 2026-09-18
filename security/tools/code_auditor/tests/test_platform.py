"""
Unit tests for Platform Client abstractions.
"""
import json
import unittest
import tempfile
import shutil
from pathlib import Path

from security.tools.code_auditor.platform.local import LocalDirectoryClient


class TestLocalPlatform(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_local_client_without_composer(self):
        client = LocalDirectoryClient(self.temp_dir)
        self.assertTrue(client.login())
        targets = client.get_targets()
        self.assertEqual(len(targets), 1)
        self.assertEqual(targets[0]["id"], "local")
        self.assertEqual(targets[0]["name"], Path(self.temp_dir).name)

    def test_local_client_with_composer(self):
        composer = Path(self.temp_dir) / "composer.json"
        composer.write_text(json.dumps({"name": "org/sample-app"}), encoding="utf-8")

        client = LocalDirectoryClient(self.temp_dir)
        targets = client.get_targets()
        self.assertEqual(len(targets), 1)
        self.assertEqual(targets[0]["name"], "org/sample-app")

    def test_local_client_submit(self):
        client = LocalDirectoryClient(self.temp_dir)
        res = client.submit("local", "payload")
        self.assertEqual(res["status"], "skipped")


if __name__ == "__main__":
    unittest.main()
