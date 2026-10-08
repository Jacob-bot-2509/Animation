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
                     summary={"command": "test", "manifest": "data/manifest.json"},
                     metrics={"n": 0},
                     env={"python": "3.14", "platform": "win", "gpu": "RTX"},
                     dirty={"clean": True, "changed": []})


class TestRunRecord(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_missing_fields_fail_fast(self):
        """msg_101-5:缺 config/git_commit/manifest_hash → fail-fast。"""
        for drop in ("config", "git_commit", "manifest_hash", "summary", "env"):
            r = _ok_record()
            if drop == "config":
                r.config = {}
            elif drop == "git_commit":
                r.git_commit = ""
            elif drop == "manifest_hash":
                r.manifest_hash = ""
            elif drop == "env":
                r.env = {}
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


class TestEnvAndFailure(unittest.TestCase):
    def test_env_recorded(self):
        r = _ok_record()
        self.assertEqual(check_record(r), [])

    def test_empty_env_fails(self):
        """R8: 空 env 必须 fail-fast。"""
        r = _ok_record()
        r.env = {}
        self.assertTrue(any("env" in p for p in check_record(r)))

    def test_failure_without_analysis_flagged(self):
        """msg_101-7:失败不留无因失败。"""
        r = _ok_record()
        r.kind = "baseline"
        r.metrics = {}
        self.assertTrue(any("failure_analysis" in p for p in check_record(r)))
        r.failure_analysis = {"reason": "OOM", "fix": "降 batch", "rollback": "runs/r0"}
        r.seed = 42  # B1: baseline 必须有 seed
        self.assertEqual(check_record(r), [])


if __name__ == "__main__":
    unittest.main()


class TestB1Snapshot(unittest.TestCase):
    def test_training_kind_requires_seed(self):
        """B1: baseline/improvement 必须有整数 seed。"""
        r = _ok_record()
        r.kind = "baseline"
        self.assertTrue(any("seed" in p for p in check_record(r)))
        r.seed = 42
        self.assertEqual(check_record(r), [])

    def test_dirty_must_be_recorded(self):
        """B1: dirty 状态必须明确记录(clean 或变更清单)。"""
        r = _ok_record()
        r.dirty = {}
        self.assertTrue(any("dirty" in p for p in check_record(r)))
        r.dirty = {"clean": True, "changed": []}
        self.assertEqual(check_record(r), [])

    def test_dirty_with_changes_recorded(self):
        """B1: dirty 变更清单明确记录也通过(不是拒绝,是可见)。"""
        r = _ok_record()
        r.dirty = {"clean": False, "changed": ["src/animtrain/validate.py"]}
        self.assertEqual(check_record(r), [])


class TestVerifyReplay(unittest.TestCase):
    """B1:完整重放校验 —— git/config/manifest 任一不一致即不可重放。"""

    def _rec(self, **over) -> dict:
        import json
        from animtrain.run_record import RunRecord
        r = RunRecord(run_id="replay-001", kind="dry-run",
                      config={"file": "configs/x.json", "sha256": "a" * 64,
                              "content": {"lr": 0.001}},
                      git_commit="c" * 40, manifest_hash="m" * 64,
                      summary={"command": "python x.py",
                               "manifest": "data/v1/manifest.json"},
                      metrics={}, env={"python": "3.13"},
                      seed=None, dirty={"clean": True, "changed": []})
        return r

    def test_matching_state_replayable(self):
        from animtrain.run_record import verify_replay
        r = self._rec()
        problems = verify_replay(r, git_commit_now="c" * 40,
                                 dirty_now={"clean": True})
        self.assertEqual(problems, [])

    def test_git_commit_mismatch_blocks(self):
        from animtrain.run_record import verify_replay
        r = self._rec()
        problems = verify_replay(r, git_commit_now="d" * 40,
                                 dirty_now={"clean": True})
        self.assertTrue(any("代码状态与记录不一致" in p for p in problems))

    def test_dirty_mismatch_blocks(self):
        from animtrain.run_record import verify_replay
        r = self._rec()
        problems = verify_replay(r, git_commit_now="c" * 40,
                                 dirty_now={"clean": False})
        self.assertTrue(any("dirty 状态与记录不一致" in p for p in problems))

    def test_config_hash_mismatch_blocks(self):
        from animtrain.run_record import verify_replay
        import tempfile
        from pathlib import Path
        r = self._rec()
        with tempfile.TemporaryDirectory() as d:
            cp = Path(d) / "config.json"
            cp.write_text('{"lr": 0.01}', encoding="utf-8")
            problems = verify_replay(r, git_commit_now="c" * 40,
                                     dirty_now={"clean": True}, config_path=cp)
            self.assertTrue(any("config 文件与记录不一致" in p for p in problems))

    def test_config_unbound_blocks(self):
        from animtrain.run_record import verify_replay
        import tempfile
        from pathlib import Path
        from animtrain.run_record import RunRecord
        r = RunRecord(run_id="replay-002", kind="baseline",
                      config={}, git_commit="c" * 40, manifest_hash="m" * 64,
                      summary={"command": "x", "manifest": "data/v1/manifest.json"},
                      metrics={}, env={"python": "3.13"},
                      seed=42, dirty={"clean": True, "changed": []})
        with tempfile.TemporaryDirectory() as d:
            cp = Path(d) / "config.json"
            cp.write_text("{}", encoding="utf-8")
            problems = verify_replay(r, git_commit_now="c" * 40,
                                     dirty_now={"clean": True}, config_path=cp)
            self.assertTrue(any("未绑定实际文件哈希" in p for p in problems))


class TestVerifyReplayGS4(unittest.TestCase):
    """GS4:dirty 内容哈希绑定 + config fail-closed。"""

    def _rec(self):
        from animtrain.run_record import RunRecord
        return RunRecord(run_id="gs4-001", kind="baseline",
                         config={"file": "configs/x.json", "sha256": "a" * 64,
                                 "content": {"lr": 0.001}},
                         git_commit="c" * 40, manifest_hash="m" * 64,
                         summary={"command": "python x.py",
                                  "manifest": "data/v1/manifest.json"},
                         metrics={}, env={"python": "3.13"},
                         seed=42, dirty={"clean": False,
                                         "changed": ["src/a.py"],
                                         "hashes": {"src/a.py": "h" * 64}})

    def test_dirty_hash_mismatch_blocks(self):
        from animtrain.run_record import verify_replay
        r = self._rec()
        problems = verify_replay(r, git_commit_now="c" * 40,
                                 dirty_now={"clean": False,
                                            "changed": ["src/a.py"],
                                            "hashes": {"src/a.py": "x" * 64}})
        self.assertTrue(any("dirty 文件内容与记录不一致" in p for p in problems))

    def test_dirty_file_set_mismatch_blocks(self):
        from animtrain.run_record import verify_replay
        r = self._rec()
        problems = verify_replay(r, git_commit_now="c" * 40,
                                 dirty_now={"clean": False,
                                            "changed": ["src/b.py"],
                                            "hashes": {"src/b.py": "h" * 64}})
        self.assertTrue(any("变更清单与记录不一致" in p for p in problems))

    def test_training_kind_config_unbound_failclosed(self):
        from animtrain.run_record import verify_replay
        r = self._rec()
        problems = verify_replay(r, git_commit_now="c" * 40,
                                 dirty_now={"clean": False,
                                            "changed": ["src/a.py"],
                                            "hashes": {"src/a.py": "h" * 64}},
                                 config_path=None)
        self.assertTrue(any("config 未绑定实际文件" in p for p in problems),
                        problems)
