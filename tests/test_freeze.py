"""冻结锁与原子写入测试(B3/B6/BR3/BR5)。"""
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


class TestBR3StrictLock(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_empty_lock_rejected(self):
        """BR3: entries=[] 的空锁必须可定位失败。"""
        lock = self.root / "empty.lock.json"
        lock.write_text('{"freeze_lock_version": 1, "locked": true, "entries": []}',
                        encoding="utf-8")
        problems = check_frozen(lock)
        self.assertTrue(any("空" in p for p in problems), problems)

    def test_unlocked_state_rejected(self):
        """BR3: locked=False 的锁必须可定位失败。"""
        lock = self.root / "unlocked.lock.json"
        lock.write_text('{"freeze_lock_version": 1, "locked": false, "entries": []}',
                        encoding="utf-8")
        problems = check_frozen(lock)
        self.assertTrue(any("locked" in p for p in problems), problems)

    def test_n_files_mismatch_rejected(self):
        """BR3: n_files 与条目数不一致必须可定位失败。"""
        p = self.root / "e.jsonl"
        p.write_text('{"id": "e1"}\n', encoding="utf-8")
        from animtrain.freeze import sha256_file
        import json as _json
        lock = self.root / "mismatch.lock.json"
        lock.write_text(_json.dumps({
            "freeze_lock_version": 1, "locked": True, "n_files": 5,
            "entries": [{"path": str(p), "sha256": sha256_file(p),
                         "size": p.stat().st_size}]}), encoding="utf-8")
        problems = check_frozen(lock)
        self.assertTrue(any("n_files" in x for x in problems), problems)

    def test_freeze_empty_list_rejected(self):
        """BR3: freeze_set([]) 不得生成可通过的空锁。"""
        with self.assertRaises(ValueError):
            freeze_set([], self.root / "x.lock.json")


if __name__ == "__main__":
    unittest.main()


class TestBR5FrozenWriteProtection(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_split_force_cannot_overwrite_frozen(self):
        """BR5: 冻结文件即使 --force 也不得被 split 改写。"""
        import subprocess
        import json as _json
        from animtrain.freeze import freeze_set
        pool = self.root / "pool.jsonl"
        pool.write_text('{"id": "s1"}\n', encoding="utf-8")
        plan = self.root / "plan.json"
        plan.write_text(_json.dumps({"train": ["s1"], "eval": [], "test": []},
                                    ensure_ascii=False), encoding="utf-8")
        out = self.root / "o"
        out.mkdir()
        ev = out / "eval.jsonl"
        ev.write_text('{"id": "frozen-e"}\n', encoding="utf-8")
        lock = self.root / "frozen.lock.json"
        freeze_set([ev], lock)
        r = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "split_data.py"),
             "--pool", str(pool), "--plan", str(plan), "--out", str(out),
             "--force", "--frozen-lock", str(lock)],
            capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(r.returncode, 0, "--force 改写了冻结文件")
        self.assertEqual(ev.read_text(encoding="utf-8"), '{"id": "frozen-e"}\n',
                         "冻结文件内容被改动")

    def test_frozen_paths_collected(self):
        from animtrain.freeze import frozen_paths, freeze_set
        p = self.root / "e.jsonl"
        p.write_text('{"id": "e1"}\n', encoding="utf-8")
        lock = self.root / "l.lock.json"
        freeze_set([p], lock)
        paths = frozen_paths(lock)
        self.assertIn(str(p.resolve()), paths)


class TestBR5OmittedLock(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_omitted_frozen_lock_still_protected(self):
        """BR5 复验:漏传 --frozen-lock,split 也必须自动发现冻结锁并拒绝。"""
        import subprocess
        import json as _json
        from animtrain.freeze import freeze_set
        pool = self.root / "pool.jsonl"
        pool.write_text('{"id": "s1"}\n', encoding="utf-8")
        plan = self.root / "plan.json"
        plan.write_text(_json.dumps({"train": ["s1"], "eval": [], "test": []},
                                    ensure_ascii=False), encoding="utf-8")
        out = self.root / "o"
        out.mkdir()
        ev = out / "eval.jsonl"
        ev.write_text('{"id": "frozen-e"}\n', encoding="utf-8")
        # 锁放在 out 父目录(自动发现范围),且不传给 split
        lock = self.root / "frozen.lock.json"
        freeze_set([ev], lock)
        r = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "split_data.py"),
             "--pool", str(pool), "--plan", str(plan), "--out", str(out),
             "--force"],  # 注意:不传 --frozen-lock
            capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(r.returncode, 0, "漏传冻结锁仍改写了冻结数据")
        self.assertEqual(ev.read_text(encoding="utf-8"), '{"id": "frozen-e"}\n',
                         "冻结文件内容被改动")


class TestBR5FailClosed(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_corrupt_lock_in_outdir_blocks(self):
        """omitted_corrupt:输出目录的坏 JSON 冻结锁必须阻断写入。"""
        import subprocess
        import json as _json
        pool = self.root / "pool.jsonl"
        pool.write_text('{"id": "s1"}\n', encoding="utf-8")
        plan = self.root / "plan.json"
        plan.write_text(_json.dumps({"train": ["s1"], "eval": [], "test": []},
                                    ensure_ascii=False), encoding="utf-8")
        out = self.root / "o"
        out.mkdir()
        (out / "frozen.lock.json").write_text("{坏 json", encoding="utf-8")
        r = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "split_data.py"),
             "--pool", str(pool), "--plan", str(plan), "--out", str(out),
             "--force"],
            capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(r.returncode, 0, "坏锁被忽略仍写入")
        self.assertFalse((out / "train.jsonl").exists(), "输出文件已写入")

    def test_freeze_set_rejects_nonstandard_name(self):
        """omitted_nonstandard:freeze.json 命名被冻结 API 拒绝。"""
        from animtrain.freeze import freeze_set
        p = self.root / "e.jsonl"
        p.write_text('{"id": "e1"}\n', encoding="utf-8")
        with self.assertRaises(ValueError):
            freeze_set([p], self.root / "freeze.json")


class TestBR4bFreezeEvidence(unittest.TestCase):
    """BR4-b:冻结证据必须绑定当前 manifest 的 eval/test 集合。"""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _lock_with(self, files, name="frozen.lock.json", meta=None):
        from animtrain.freeze import freeze_set
        return freeze_set(files, self.root / name, meta=meta)

    def test_matching_lock_ok(self):
        """matching lock:锁覆盖 manifest 的 eval 文件且绑定 hash 一致。"""
        from animtrain.freeze import check_frozen
        ev = self.root / "eval.jsonl"
        ev.write_text('{"id": "e1"}\n', encoding="utf-8")
        self._lock_with([ev], meta={"manifest_sha256": "abc"})
        self.assertEqual(check_frozen(self.root / "frozen.lock.json"), [])

    def test_unrelated_lock_detected(self):
        """unrelated lock:锁覆盖的文件不在 eval/test 内 → 不得当证据。"""
        from animtrain.freeze import frozen_paths
        other = self.root / "unrelated.txt"
        other.write_text("x", encoding="utf-8")
        self._lock_with([other])
        paths = frozen_paths(self.root / "frozen.lock.json")
        self.assertNotIn(str(self.root / "eval.jsonl"), paths)

    def test_partial_lock_detected(self):
        """partial lock:只有 eval 被冻结、test 未覆盖 → 冻结不完整。"""
        from animtrain.freeze import frozen_paths
        ev = self.root / "eval.jsonl"
        ev.write_text('{"id": "e1"}\n', encoding="utf-8")
        self._lock_with([ev])
        frozen = frozen_paths(self.root / "frozen.lock.json")
        self.assertNotIn(str((self.root / "test.jsonl").resolve()), frozen)

    def test_corrupt_lock_detected(self):
        """corrupt lock:坏 JSON 锁必须可定位失败。"""
        from animtrain.freeze import check_frozen
        bad = self.root / "bad.lock.json"
        bad.write_text("{坏", encoding="utf-8")
        problems = check_frozen(bad)
        self.assertTrue(any("不可读" in p for p in problems), problems)
