import io
import sys
import tempfile
import unittest
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import patch


TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import dfir_query


class _Boot:
    ClustersPerFileRecordSegment = -10


class _Ntfs:
    boot_sector = _Boot()
    cluster_size = 4096


class _Fs:
    ntfs = _Ntfs()


class DfirQueryTests(unittest.TestCase):
    def test_stream_search_finds_match_across_chunk_boundary_without_duplicate(self):
        handle = io.BytesIO(b"A" * 7 + b"needle" + b"B" * 7)
        hits = dfir_query.stream_search(
            handle,
            [("ascii", b"needle")],
            chunk_size=8,
            max_hits=10,
        )
        self.assertEqual(hits, [{"encoding": "ascii", "offset": 7}])

    def test_stream_search_supports_ascii_and_utf16(self):
        blob = b"xsecretx" + "secret".encode("utf-16le")
        hits = dfir_query.stream_search(
            io.BytesIO(blob),
            [("ascii", b"secret"), ("utf16le", "secret".encode("utf-16le"))],
            chunk_size=5,
            max_hits=10,
        )
        self.assertEqual(
            [(row["encoding"], row["offset"]) for row in hits],
            [("ascii", 1), ("utf16le", 8)],
        )

    def test_mft_record_size_handles_negative_ntfs_encoding(self):
        self.assertEqual(dfir_query._mft_record_size(_Fs()), 1024)

    def test_copy_stream_hashes_while_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "out.bin"
            result = dfir_query.copy_stream(io.BytesIO(b"abc"), target, chunk_size=2)
            self.assertEqual(result["size"], 3)
            self.assertEqual(
                result["sha256"],
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            )
            self.assertEqual(target.read_bytes(), b"abc")

    def test_copy_stream_refuses_to_overwrite_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "out.bin"
            target.write_bytes(b"original")
            with self.assertRaisesRegex(ValueError, "refusing to overwrite"):
                dfir_query.copy_stream(io.BytesIO(b"replacement"), target)
            self.assertEqual(target.read_bytes(), b"original")

    def test_preflight_fails_closed_when_backend_import_is_unavailable(self):
        with patch.object(
            dfir_query,
            "load_backend",
            side_effect=dfir_query.BackendUnavailable("fixture missing"),
        ):
            result = dfir_query.preflight()
        self.assertFalse(result["ready"])
        self.assertTrue(any("backend import failed" in item for item in result["errors"]))

    def test_preflight_can_inventory_extracted_evidence_root(self):
        fake_backend = SimpleNamespace(target_version=dfir_query.PINNED_DISSECT_TARGET)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Windows/System32/config").mkdir(parents=True)
            (root / "Windows/System32/config/SYSTEM").write_bytes(b"hive")
            (root / "Windows/System32/SRU").mkdir(parents=True)
            (root / "Windows/System32/SRU/SRUDB.dat").write_bytes(b"srum")
            (root / "Users/u/Recent").mkdir(parents=True)
            (root / "Users/u/Recent/a.lnk").write_bytes(b"lnk")
            with patch.object(dfir_query, "load_backend", return_value=fake_backend), patch.object(
                dfir_query, "load_ese_backend", return_value=dfir_query.PINNED_DISSECT_ESEDB
            ):
                result = dfir_query.preflight(evidence_root=root)
        self.assertTrue(result["ready"])
        self.assertEqual(result["evidence_root"]["artifact_signals"]["registry_hives"], 1)
        self.assertEqual(result["evidence_root"]["artifact_signals"]["srum"], 1)
        self.assertEqual(result["evidence_root"]["artifact_signals"]["lnk"], 1)
        self.assertTrue(result["capabilities"]["ese"])

    def test_preflight_fails_when_ese_artifacts_exist_without_ese_parser(self):
        fake_backend = SimpleNamespace(target_version=dfir_query.PINNED_DISSECT_TARGET)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Windows/System32/SRU").mkdir(parents=True)
            (root / "Windows/System32/SRU/SRUDB.dat").write_bytes(b"srum")
            with patch.object(dfir_query, "load_backend", return_value=fake_backend), patch.object(
                dfir_query,
                "load_ese_backend",
                side_effect=dfir_query.BackendUnavailable("fixture no ESE"),
            ):
                result = dfir_query.preflight(evidence_root=root)
        self.assertFalse(result["ready"])
        self.assertFalse(result["capabilities"]["ese"])
        self.assertTrue(any("ESE" in item for item in result["errors"]))


if __name__ == "__main__":
    unittest.main()
