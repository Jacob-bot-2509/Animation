"""Regression checks for exact $I decoding and honest incomplete-scan results."""
import importlib.util
import json
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "holdout_recyclebin_scan_tested", ROOT / "tools/holdout_recyclebin_scan.py")
scan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scan)


def blob(path=r"D:\Animation-Model-Training\outputs\screening-tmp", version=2, ticks=123456789):
    field = (path + "\x00").encode("utf-16-le")
    head = struct.pack("<QQQ", version, 123, ticks)
    if version == 1:
        return head + field.ljust(520, b"\x00")
    return head + struct.pack("<I", len(field) // 2) + field


class MetadataTests(unittest.TestCase):
    def test_v1_fixed_field(self):
        value = scan.parse_i_metadata(blob(version=1))
        self.assertEqual(value["format_version"], 1)
        self.assertEqual(value["original_path"], r"D:\Animation-Model-Training\outputs\screening-tmp")

    def test_v2_starts_at_28_not_24(self):
        value = scan.parse_i_metadata(blob())
        self.assertEqual(value["original_path"], r"D:\Animation-Model-Training\outputs\screening-tmp")
        self.assertEqual(value["original_size_bytes"], 123)

    def test_unicode_surrogate_pair_count(self):
        path = "D:\\\u6570\u636e\\\U0001f600.jsonl"
        self.assertEqual(scan.parse_i_metadata(blob(path))["original_path"], path)

    def test_filetime_exact_seven_digits(self):
        self.assertEqual(scan.parse_i_metadata(blob())["deleted_at_utc"],
                         "1601-01-01T00:00:12.3456789Z")

    def test_bad_version_and_headers(self):
        for raw in [b"", b"\x00" * 23, struct.pack("<QQQ", 3, 1, 1),
                    struct.pack("<QQQ", 2, 1, 1), blob(version=1)[:-2]]:
            with self.subTest(length=len(raw)), self.assertRaises(ValueError):
                scan.parse_i_metadata(raw)

    def test_v2_count_and_truncation(self):
        raw = blob()
        for bad in [raw[:-2], raw + b"\x00\x00", raw[:24] + struct.pack("<I", 0) + raw[28:]]:
            with self.subTest(length=len(bad)), self.assertRaises(ValueError):
                scan.parse_i_metadata(bad)

    def test_invalid_utf16_rejected(self):
        raw = struct.pack("<QQQI", 2, 1, 0, 2) + b"\x00\xd8\x00\x00"
        with self.assertRaises(ValueError):
            scan.parse_i_metadata(raw)

    def test_terminator_and_absolute_path(self):
        for path in [r"relative\name", "D:\\a\x00b"]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                scan.parse_i_metadata(blob(path))
        raw = blob()[:-2] + b"x\x00"
        with self.assertRaises(ValueError):
            scan.parse_i_metadata(raw)

    def test_filetime_overflow(self):
        with self.assertRaises(ValueError):
            scan.parse_i_metadata(blob(ticks=(1 << 64) - 1))

    def test_path_relation_component_boundaries(self):
        parent = r"D:\Animation-Model-Training"
        self.assertEqual(scan.path_relation(parent, parent + r"\data\a.jsonl"),
                         "DELETED_ANCESTOR_CONTAINS_TARGET")
        self.assertEqual(scan.path_relation(parent.lower(), parent), "EXACT_PATH")
        self.assertIsNone(scan.path_relation(parent, parent + "-copy"))


class ScanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(
            prefix="recycle-metadata-fixture-", dir=ROOT / "reviews/codex-supervision/2026-10-07-historical-gap-mail-review")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.sid = self.root / "S-1-5-21-TEST"
        self.sid.mkdir()

    def test_current_snapshot_no_historical_claim(self):
        (self.sid / "$I1").write_bytes(blob())
        (self.sid / "$R1").write_bytes(b"PAYLOAD MUST NOT BE OPENED")
        report = scan.scan_current_metadata(self.root, [r"D:\Animation-Model-Training"])
        self.assertEqual(report["status"], "SNAPSHOT_COMPLETE")
        self.assertEqual(report["parsed_records"], 1)
        self.assertEqual(report["matched_records"], 1)
        self.assertFalse(report["historical_non_deletion_proved"])

    def test_bad_item_keeps_good_item_and_fails_coverage(self):
        (self.sid / "$IBAD").write_bytes(b"bad")
        (self.sid / "$IGOOD").write_bytes(blob())
        report = scan.scan_current_metadata(self.root)
        self.assertEqual(report["parsed_records"], 1)
        self.assertEqual(report["metadata_files_seen"], 2)
        self.assertEqual(report["status"], "SNAPSHOT_INCOMPLETE")
        self.assertEqual(len(report["errors"]), 1)

    def test_permission_error_is_not_empty_success(self):
        original = scan.os.scandir
        def denied(path):
            if str(path) == str(self.sid):
                raise PermissionError("fixture permission denied")
            return original(path)
        with patch.object(scan.os, "scandir", side_effect=denied):
            report = scan.scan_current_metadata(self.root)
        self.assertEqual(report["status"], "SNAPSHOT_INCOMPLETE")
        self.assertEqual(report["errors"][0]["exception_type"], "PermissionError")

    def test_reparse_metadata_not_followed(self):
        (self.sid / "$I1").write_bytes(blob())
        original = scan.is_reparse
        with patch.object(scan, "is_reparse", side_effect=lambda s: s.st_size == len(blob()) or original(s)):
            report = scan.scan_current_metadata(self.root)
        self.assertEqual(report["parsed_records"], 0)
        self.assertEqual(report["status"], "SNAPSHOT_INCOMPLETE")

    def test_missing_root_returns_incomplete_cli(self):
        missing = self.root / "missing"
        with patch("builtins.print") as output:
            self.assertEqual(scan.main(["--root", str(missing)]), 2)
        self.assertEqual(json.loads(output.call_args.args[0])["status"], "SNAPSHOT_INCOMPLETE")


if __name__ == "__main__":
    unittest.main()
