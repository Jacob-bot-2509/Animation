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
    def test_status_reports_not_generated(self):
        out = run("status")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertIn("未生成", out.stdout)
        self.assertIn("未冻结", out.stdout)

    def test_check_empty_dir_reports_truthfully(self):
        out = run("check", ROOT / "data/v1/eval")
        self.assertEqual(out.returncode, 0)
        self.assertIn("未生成任何样本", out.stdout)

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
