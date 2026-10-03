"""eval/test 准备接口测试(msg_199):status/check/freeze 契约。
synthetic fixtures 只在 reviews/fixtures-eval-test/,不混入正式数据。"""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools" / "eval_test_prep.py"
FIX = ROOT / "reviews" / "fixtures-eval-test"


def run(*args) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-X", "utf8", str(CLI), *map(str, args)],
                          capture_output=True, encoding="utf-8", errors="replace")


class TestEvalTestPrep(unittest.TestCase):
    def test_status_reports_generated_and_frozen(self):
        """2026-10-03 起 eval/test 已生成并冻结:status 如实报告。"""
        out = run("status")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertIn("已生成", out.stdout)
        self.assertIn("冻结锁", out.stdout)

    def test_check_empty_dir_reports_truthfully(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            empty = Path(d)
            out = run("check", empty)
            self.assertEqual(out.returncode, 0)
            self.assertIn("未生成任何样本", out.stdout)

    def test_check_generated_eval_passes(self):
        out = run("check", ROOT / "data/v1/eval", "--train-dir", ROOT / "data/v1/raw")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertIn("通过", out.stdout)

    def test_status_bad_lock_not_reported_as_frozen(self):
        """msg_256 探针:坏 JSON 锁不得冒充有效冻结(status 须校验而非只看存在)。"""
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            ev = base / "eval"
            ev.mkdir()
            (ev / "dataset_eval.jsonl").write_text(
                '{"id": "x", "category": "c", "sub_category": "s", "problem": "p", '
                '"solution": "s", "answer": "a", '
                '"scene_spec": {"objects": ["o"], "steps": ["t"]}, '
                '"source": "self-authored", "license": "Internal-Research-Use-Only"}\n',
                encoding="utf-8")
            (base / "eval-broken.lock.json").write_text("{not valid json",
                                                        encoding="utf-8")
            out = run("status", "--dir", base)
            self.assertEqual(out.returncode, 0)
            self.assertIn("校验未过", out.stdout)
            self.assertNotIn("校验通过", out.stdout)

    def test_check_flags_train_leak(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            td = Path(d)
            train_dir = td / "train"
            train_dir.mkdir()
            (train_dir / "train.jsonl").write_text(
                (FIX / "train_synthetic.jsonl").read_text(encoding="utf-8"),
                encoding="utf-8")
            leak = td / "eval.jsonl"
            leak.write_text((FIX / "eval_leak.jsonl").read_text(encoding="utf-8"),
                            encoding="utf-8")
            out = run("check", leak, "--train-dir", train_dir)
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertIn("精确重叠", out.stdout)

    def test_check_independent_eval_passes(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            td = Path(d)
            train_dir = td / "train"
            train_dir.mkdir()
            (train_dir / "train.jsonl").write_text(
                (FIX / "train_synthetic.jsonl").read_text(encoding="utf-8"),
                encoding="utf-8")
            ok = td / "eval.jsonl"
            ok.write_text((FIX / "eval_ok.jsonl").read_text(encoding="utf-8"),
                          encoding="utf-8")
            out = run("check", ok, "--train-dir", train_dir)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertIn("隔离检查通过", out.stdout)

    def test_freeze_refused(self):
        out = run("freeze", ROOT / "data/v1/eval")
        self.assertEqual(out.returncode, 2)
        self.assertIn("未授权", out.stdout)


if __name__ == "__main__":
    unittest.main()
