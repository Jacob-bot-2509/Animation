"""冻结锁测试(B3:冻结后不可变,哈希变化大声失败)。"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.freeze import check_frozen, freeze_set  # noqa: E402


class TestFreeze(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_freeze_then_clean(self):
        p = self.root / "eval.jsonl"
        p.write_text('{"id": "e1"}\n', encoding="utf-8")
        lock = self.root / "eval.lock.json"
        freeze_set([p], lock, meta={"name": "eval-v1"})
        self.assertEqual(check_frozen(lock), [])

    def test_modified_after_freeze_detected(self):
        """冻结后改一个字节 → 哈希变化必须检出。"""
        p = self.root / "eval.jsonl"
        p.write_text('{"id": "e1"}\n', encoding="utf-8")
        lock = self.root / "eval.lock.json"
        freeze_set([p], lock)
        p.write_text('{"id": "e1"}\n{"id": "e2"}\n', encoding="utf-8")
        problems = check_frozen(lock)
        self.assertTrue(any("哈希变化" in x for x in problems), problems)

    def test_deleted_after_freeze_detected(self):
        p = self.root / "eval.jsonl"
        p.write_text('{"id": "e1"}\n', encoding="utf-8")
        lock = self.root / "eval.lock.json"
        freeze_set([p], lock)
        p.unlink()
        problems = check_frozen(lock)
        self.assertTrue(any("不存在" in x for x in problems), problems)

    def test_relock_rejected(self):
        """已有锁拒绝重新生成(冻结后不可重新生成,防静默换集)。"""
        p = self.root / "eval.jsonl"
        p.write_text('{"id": "e1"}\n', encoding="utf-8")
        lock = self.root / "eval.lock.json"
        freeze_set([p], lock)
        with self.assertRaises(ValueError):
            freeze_set([p], lock)


class TestAtomicWrite(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_atomic_write_and_no_leftover(self):
        from animtrain.atomic_write import atomic_write_text
        p = self.root / "out" / "x.json"
        atomic_write_text(p, '{"a": 1}')
        self.assertEqual(p.read_text(encoding="utf-8"), '{"a": 1}')
        # 无 .tmp 残留
        self.assertEqual(list(p.parent.glob("*.tmp")), [])

    def test_atomic_write_overwrite_is_complete(self):
        from animtrain.atomic_write import atomic_write_text
        p = self.root / "x.json"
        atomic_write_text(p, "old")
        atomic_write_text(p, "new" * 1000)
        self.assertEqual(len(p.read_text(encoding="utf-8")), 3000)


if __name__ == "__main__":
    unittest.main()
