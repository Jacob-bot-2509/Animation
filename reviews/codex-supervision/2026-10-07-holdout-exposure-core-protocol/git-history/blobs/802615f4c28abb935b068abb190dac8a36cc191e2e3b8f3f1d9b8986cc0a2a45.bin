"""多文件发布事务测试(B6):整组成功/失败回滚/中断恢复/冻结保护。"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.publish import (  # noqa: E402
    BACKUP_SUFFIX, publish_files, recover_publish, journal_path)


class TestPublish(unittest.TestCase):
    def test_publish_all_success_clean_state(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            a, b = d / "a.txt", d / "sub" / "b.txt"
            out = publish_files(d, "g1", [(a, "内容A"), (b, "内容B")])
            self.assertEqual(out, [a, b])
            self.assertEqual(a.read_text(encoding="utf-8"), "内容A")
            self.assertEqual(b.read_text(encoding="utf-8"), "内容B")
            self.assertFalse(journal_path(d, "g1").exists())
            self.assertEqual(list(d.rglob(f"*{BACKUP_SUFFIX}")), [])

    def test_refuse_overwrite_without_force(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            a = d / "a.txt"
            a.write_text("old", encoding="utf-8")
            with self.assertRaises(ValueError):
                publish_files(d, "g2", [(a, "new")])
            self.assertEqual(a.read_text(encoding="utf-8"), "old")

    def test_failure_rolls_back_written_files(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            a = d / "a.txt"
            a.write_text("oldA", encoding="utf-8")
            bad = d / "bad"
            bad.mkdir()  # 目标是个目录 → 原子写必失败
            with self.assertRaises(OSError):
                publish_files(d, "g3", [(a, "newA"), (bad, "x")], force=True)
            self.assertEqual(a.read_text(encoding="utf-8"), "oldA")  # 已回滚
            self.assertFalse(journal_path(d, "g3").exists())  # journal 已清

    def test_recover_rollback_after_interrupt(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            a = d / "a.txt"
            a.write_text("损坏的新内容", encoding="utf-8")
            backup = Path(str(a) + BACKUP_SUFFIX)
            backup.write_text("原始内容", encoding="utf-8")
            jp = journal_path(d, "g4")
            jp.write_text(json.dumps(
                {"group": "g4", "items": [{"path": str(a.resolve()),
                                           "backup": str(backup.resolve())}]},
                ensure_ascii=False), encoding="utf-8")
            result = recover_publish(d, "g4", rollback=True)
            self.assertTrue(result["recovered"])
            self.assertEqual(a.read_text(encoding="utf-8"), "原始内容")
            self.assertFalse(jp.exists())

    def test_publish_refuses_frozen_target(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            a = d / "frozen.jsonl"
            a.write_text("old", encoding="utf-8")
            lock = {"freeze_lock_version": 1, "locked": True,
                    "entries": [{"path": str(a.resolve()), "sha256": "x" * 64,
                                 "size": 0}], "n_files": 1}
            (d / "f.lock.json").write_text(json.dumps(lock), encoding="utf-8")
            with self.assertRaises(ValueError) as ctx:
                publish_files(d, "g5", [(a, "new")], force=True)
            self.assertIn("冻结", str(ctx.exception))
            self.assertEqual(a.read_text(encoding="utf-8"), "old")

    def test_leftover_journal_must_recover_first(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            jp = journal_path(d, "g6")
            jp.write_text("{}", encoding="utf-8")
            with self.assertRaises(ValueError):
                publish_files(d, "g6", [(d / "a.txt", "x")])


if __name__ == "__main__":
    unittest.main()
