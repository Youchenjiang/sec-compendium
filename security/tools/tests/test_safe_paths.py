"""Tests for ``security/tools/safe_paths.py``."""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import safe_paths  # noqa: E402


class JoinWithinTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)

    def test_relative_child_stays_inside(self):
        target = safe_paths.join_within(self.base, "Users", "a.txt")
        self.assertEqual(target, (self.base / "Users" / "a.txt").resolve())

    def test_parent_escape_is_refused(self):
        with self.assertRaises(safe_paths.UnsafePathError):
            safe_paths.join_within(self.base, "../outside.txt")

    def test_nested_escape_is_refused(self):
        with self.assertRaises(safe_paths.UnsafePathError):
            safe_paths.join_within(self.base, "a/../../outside.txt")


class ResolveCliPathTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_temp_directory_is_allowed(self):
        path = self.root / "evidence.log"
        self.assertEqual(safe_paths.resolve_cli_path(path), path.resolve())

    def test_path_outside_every_root_is_refused(self):
        with patch.object(safe_paths, "allowed_roots", return_value=[self.root / "only"]):
            with self.assertRaises(safe_paths.UnsafePathError):
                safe_paths.resolve_cli_path(self.root / "elsewhere" / "x.csv")

    def test_extra_roots_come_from_the_environment(self):
        extra = (self.root / "extra").resolve()
        with patch.dict(os.environ, {"SECURITY_TOOLS_ALLOWED_ROOTS": str(extra)}):
            self.assertIn(extra, safe_paths.allowed_roots())

    def test_lab_data_root_comes_from_the_environment(self):
        lab = (self.root / "lab").resolve()
        with patch.dict(os.environ, {"SECURITY_LAB_DATA_ROOT": str(lab)}):
            self.assertIn(lab, safe_paths.allowed_roots())


if __name__ == "__main__":
    unittest.main()
