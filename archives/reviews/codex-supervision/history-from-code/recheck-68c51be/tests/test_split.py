"""split 工具测试(测试先行:确定性/ID 清单分配/失败保留样本与原因)。"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def _run_split(pool: Path, plan: Path, out: Path, extra: list[str] | None = None):
    r = subprocess.run(
        [str(PY), str(ROOT / "tools" / "split_data.py"),
         "--pool", str(pool), "--plan", str(plan), "--out", str(out),
         "--allow-empty"]  # 既有用例专注分配语义;C2 空集合拒绝单独测试
        + (extra or []),
        capture_output=True, text=True, encoding="utf-8")
    return r


class TestSplit(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.pool = self.root / "pool.jsonl"
        self.pool.write_text("\n".join([
            '{"id": "s1", "problem": "题1"}',
            '{"id": "s2", "problem": "题2"}',
            '{"id": "s3", "problem": "题3"}',
            '{"id": "s4", "problem": "题4"}',
        ]) + "\n", encoding="utf-8")
        self.plan = self.root / "plan.json"
        self.plan.write_text(json.dumps({
            "train": ["s1", "s2"], "eval": ["s3"], "test": ["s4"]},
            ensure_ascii=False, indent=2), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_deterministic_same_hash(self):
        """msg_101-3:同一配置重复 dry-run 结果 hash 一致。"""
        out1, out2 = self.root / "o1", self.root / "o2"
        r1 = _run_split(self.pool, self.plan, out1)
        r2 = _run_split(self.pool, self.plan, out2)
        self.assertEqual(r1.returncode, 0, r1.stderr)
        self.assertEqual(r2.returncode, 0, r2.stderr)
        for f in ("train.jsonl", "eval.jsonl", "test.jsonl"):
            self.assertEqual((out1 / f).read_text(encoding="utf-8"),
                             (out2 / f).read_text(encoding="utf-8"),
                             f"{f} 两次运行内容不一致")

    def test_plan_distribution(self):
        out = self.root / "o"
        r = _run_split(self.pool, self.plan, out)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual([json.loads(l)["id"] for l in
                          (out / "train.jsonl").read_text(encoding="utf-8").splitlines()],
                         ["s1", "s2"])
        self.assertEqual([json.loads(l)["id"] for l in
                          (out / "eval.jsonl").read_text(encoding="utf-8").splitlines()],
                         ["s3"])
        self.assertEqual([json.loads(l)["id"] for l in
                          (out / "test.jsonl").read_text(encoding="utf-8").splitlines()],
                         ["s4"])

    def test_pool_sample_not_in_plan_rejected_with_reason(self):
        """msg_101-3:失败保留原始 sample_id 与原因(池里有但计划没分配)。"""
        plan = self.root / "plan2.json"
        plan.write_text(json.dumps({"train": ["s1"], "eval": ["s3"], "test": []},
                                   ensure_ascii=False), encoding="utf-8")
        out = self.root / "o"
        r = _run_split(self.pool, plan, out)
        self.assertEqual(r.returncode, 0, r.stderr)
        rej = [json.loads(l) for l in
               (out / "rejected.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertTrue(any(x["sample_id"] == "s2" for x in rej), rej)
        self.assertTrue(any("未分配" in x.get("reason", "") for x in rej), rej)

    def test_plan_id_missing_in_pool_rejected_with_reason(self):
        """msg_101-3:计划里有但池子缺的样本,记录原因不静默。"""
        plan = self.root / "plan3.json"
        plan.write_text(json.dumps({"train": ["s1", "ghost"], "eval": [], "test": []},
                                   ensure_ascii=False), encoding="utf-8")
        out = self.root / "o"
        r = _run_split(self.pool, plan, out)
        self.assertEqual(r.returncode, 0, r.stderr)
        rej = [json.loads(l) for l in
               (out / "rejected.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertTrue(any(x["sample_id"] == "ghost" and "池中缺失" in x["reason"]
                            for x in rej), rej)

    def test_dry_run_writes_nothing(self):
        out = self.root / "o"
        r = _run_split(self.pool, self.plan, out, extra=["--dry-run"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(out.exists(), "dry-run 不应写文件")
        self.assertIn("dry-run", r.stdout)


if __name__ == "__main__":
    unittest.main()
