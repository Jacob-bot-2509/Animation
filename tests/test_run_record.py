"""运行记录测试(msg_101-5:config 快照/git commit/manifest hash/摘要/指标,
缺失 fail-fast,dry-run 可重放)。"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.run_record import RunRecord, check_record  # noqa: E402


def _ok_record() -> RunRecord:
    return RunRecord(run_id="r1", kind="dry-run", config={"a": 1},
                     git_commit="abc1234", manifest_hash="f" * 64,
                     summary={"command": "test"}, metrics={"n": 0})


class TestRunRecord(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_missing_fields_fail_fast(self):
        """msg_101-5:缺 config/git_commit/manifest_hash → fail-fast。"""
        for drop in ("config", "git_commit", "manifest_hash", "summary"):
            r = _ok_record()
            if drop == "config":
                r.config = {}
            elif drop == "git_commit":
                r.git_commit = ""
            elif drop == "manifest_hash":
                r.manifest_hash = ""
            else:
                r.summary = {}
            problems = check_record(r)
            self.assertTrue(any(drop in p or "config" in p for p in problems),
                            f"{drop} 缺失未 fail-fast: {problems}")

    def test_ok_record_passes(self):
        self.assertEqual(check_record(_ok_record()), [])

    def test_roundtrip(self):
        r = _ok_record()
        p = self.root / "run_record.json"
        r.save(p)
        loaded = RunRecord.load(p)
        self.assertEqual(loaded.to_dict(), r.to_dict())

    def test_manifest_hash_verifiable(self):
        """manifest hash 必须能对实际文件重算验证(dry-run 可重放的依据)。"""
        f = self.root / "manifest.json"
        f.write_text('{"name": "t"}', encoding="utf-8")
        import hashlib
        r = _ok_record()
        r.manifest_hash = hashlib.sha256(f.read_bytes()).hexdigest()
        self.assertEqual(check_record(r, manifest_path=f), [])
        r.manifest_hash = "0" * 64
        self.assertTrue(any("manifest hash" in p for p in check_record(r, manifest_path=f)))


if __name__ == "__main__":
    unittest.main()
