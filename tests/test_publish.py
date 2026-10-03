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
                {"group": "g4", "stage": "writing", "committed": [], "restored": [],
                 "items": [{"path": str(a.resolve()),
                            "backup": str(backup.resolve()),
                            "existed_before": True,
                            "hash_old": "oldhash", "hash_new": "newhash"}]},
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


class TestPublishGS1(unittest.TestCase):
    """GS1 反例:重复目标/备份碰撞/清理失败不回滚/恢复冻结保护。"""

    def test_duplicate_targets_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            a = d / "a.txt"
            with self.assertRaises(ValueError) as ctx:
                publish_files(d, "g7", [(a, "x"), (a, "y")])
            self.assertIn("重复目标", str(ctx.exception))

    def test_backup_collision_rejected_and_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            a = d / "a.txt"
            a.write_text("old", encoding="utf-8")
            bak = Path(str(a) + BACKUP_SUFFIX)
            bak.write_text("既有备份", encoding="utf-8")
            with self.assertRaises(ValueError) as ctx:
                publish_files(d, "g8", [(a, "new")], force=True)
            self.assertIn("碰撞", str(ctx.exception))
            self.assertEqual(bak.read_text(encoding="utf-8"), "既有备份")  # 未删
            self.assertEqual(a.read_text(encoding="utf-8"), "old")

    def test_cleanup_failure_keeps_journal_and_backups(self):
        from unittest import mock
        from animtrain import publish as pub_mod
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            a = d / "a.txt"
            a.write_text("oldA", encoding="utf-8")
            real_unlink = Path.unlink

            def failing_unlink(self, *args, **kwargs):
                if self.name.endswith(BACKUP_SUFFIX):
                    raise OSError("模拟清理失败")
                return real_unlink(self, *args, **kwargs)

            with mock.patch.object(Path, "unlink", failing_unlink):
                with self.assertRaises(pub_mod.PublishCleanupError):
                    publish_files(d, "g9", [(a, "newA")], force=True)
            # 不回滚:新内容保留,备份与 journal 保留交人工
            self.assertEqual(a.read_text(encoding="utf-8"), "newA")
            self.assertTrue(journal_path(d, "g9").exists())
            self.assertTrue(Path(str(a) + BACKUP_SUFFIX).exists())

    def test_recover_removes_new_file_leftover(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            a = d / "new.txt"  # 发布时不存在(existed_before=False)
            a.write_text("残留新文件", encoding="utf-8")
            jp = journal_path(d, "g10")
            jp.write_text(json.dumps(
                {"group": "g10", "stage": "writing", "committed": [], "restored": [],
                 "items": [{"path": str(a.resolve()),
                            "backup": str(a.resolve()) + BACKUP_SUFFIX,
                            "existed_before": False,
                            "hash_old": "", "hash_new": "nh"}]},
                ensure_ascii=False), encoding="utf-8")
            result = recover_publish(d, "g10", rollback=True)
            self.assertTrue(result["recovered"])
            self.assertFalse(a.exists())  # 残留已删

    def test_recover_refuses_frozen_target(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            a = d / "frozen.jsonl"
            a.write_text("被改坏的冻结数据", encoding="utf-8")
            backup = Path(str(a) + BACKUP_SUFFIX)
            backup.write_text("冻结原始内容", encoding="utf-8")
            lock = {"freeze_lock_version": 1, "locked": True,
                    "entries": [{"path": str(a.resolve()), "sha256": "x" * 64,
                                 "size": 0}], "n_files": 1}
            (d / "f.lock.json").write_text(json.dumps(lock), encoding="utf-8")
            jp = journal_path(d, "g11")
            jp.write_text(json.dumps(
                {"group": "g11", "stage": "writing", "committed": [], "restored": [],
                 "items": [{"path": str(a.resolve()),
                            "backup": str(backup.resolve()),
                            "existed_before": True,
                            "hash_old": "oh", "hash_new": "nh"}]},
                ensure_ascii=False), encoding="utf-8")
            result = recover_publish(d, "g11", rollback=True)
            self.assertFalse(result["recovered"])
            self.assertIn("冻结", result.get("error", ""))
            self.assertTrue(jp.exists())  # 保留现场

    def test_recover_corrupt_journal_failclosed(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            jp = journal_path(d, "g12")
            jp.write_text("not json", encoding="utf-8")
            result = recover_publish(d, "g12", rollback=True)
            self.assertFalse(result["recovered"])
            self.assertIn("损坏", result.get("error", ""))
            self.assertTrue(jp.exists())  # 不删除


class TestPublishMsg216(unittest.TestCase):
    """msg_216 反例:命名空间互斥/阶段感知/幂等回滚/冻结新文件/严格 schema。"""

    def _journal(self, d: Path, name: str, stage: str, items: list[dict]):
        jp = journal_path(d, name)
        jp.write_text(json.dumps({"group": name, "stage": stage,
                                  "committed": [], "restored": [], "items": items},
                                 ensure_ascii=False), encoding="utf-8")
        return jp

    def test_target_backup_namespace_overlap_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            a = d / "a.txt"
            with self.assertRaises(ValueError) as ctx:
                publish_files(d, "g13", [(a, "x"), (Path(str(a) + BACKUP_SUFFIX), "y")],
                              force=True)
            self.assertIn("备份路径与", str(ctx.exception))
            self.assertFalse(a.exists())  # 预验失败,未写任何文件

    def test_target_journal_overlap_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            jp = journal_path(d, "g14")
            with self.assertRaises(ValueError) as ctx:
                publish_files(d, "g14", [(jp, "x")], force=True)
            self.assertIn("journal", str(ctx.exception))

    def test_cleanup_stage_forward_only(self):
        """已提交组(stage=cleanup)绝不回滚,只清理备份。"""
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            a = d / "a.txt"
            a.write_text("newA", encoding="utf-8")  # 已提交的新内容
            backup = Path(str(a) + BACKUP_SUFFIX)
            backup.write_text("oldA", encoding="utf-8")
            self._journal(d, "g15", "cleanup",
                          [{"path": str(a.resolve()),
                            "backup": str(backup.resolve()),
                            "existed_before": True,
                            "hash_old": "oh", "hash_new": "nh"}])
            result = recover_publish(d, "g15", rollback=True)
            self.assertTrue(result["recovered"])
            self.assertEqual(a.read_text(encoding="utf-8"), "newA")  # 未回滚
            self.assertFalse(backup.exists())  # 备份已清理

    def test_rollback_idempotent(self):
        """目标已是原内容(hash 匹配)→ 幂等跳过,不重复恢复不报错。"""
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            a = d / "a.txt"
            a.write_text("oldA", encoding="utf-8")
            import hashlib
            old_hash = hashlib.sha256(b"oldA").hexdigest()
            backup = Path(str(a) + BACKUP_SUFFIX)
            backup.write_text("oldA", encoding="utf-8")
            self._journal(d, "g16", "writing",
                          [{"path": str(a.resolve()),
                            "backup": str(backup.resolve()),
                            "existed_before": True,
                            "hash_old": old_hash, "hash_new": "nh"}])
            result = recover_publish(d, "g16", rollback=True)
            self.assertTrue(result["recovered"], result)
            self.assertEqual(a.read_text(encoding="utf-8"), "oldA")
            self.assertFalse(journal_path(d, "g16").exists())

    def test_frozen_new_file_not_deleted(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            a = d / "new.jsonl"
            a.write_text("残留新文件", encoding="utf-8")
            lock = {"freeze_lock_version": 1, "locked": True,
                    "entries": [{"path": str(a.resolve()), "sha256": "x" * 64,
                                 "size": 0}], "n_files": 1}
            (d / "f.lock.json").write_text(json.dumps(lock), encoding="utf-8")
            self._journal(d, "g17", "writing",
                          [{"path": str(a.resolve()),
                            "backup": str(a.resolve()) + BACKUP_SUFFIX,
                            "existed_before": False,
                            "hash_old": "", "hash_new": "nh"}])
            result = recover_publish(d, "g17", rollback=True)
            self.assertFalse(result["recovered"])
            self.assertIn("冻结", result.get("error", ""))
            self.assertTrue(a.exists())  # 冻结新文件未被删除

    def test_empty_object_journal_failclosed(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            jp = journal_path(d, "g18")
            jp.write_text("{}", encoding="utf-8")
            result = recover_publish(d, "g18", rollback=True)
            self.assertFalse(result["recovered"])
            self.assertIn("缺", result.get("error", ""))
            self.assertTrue(jp.exists())
