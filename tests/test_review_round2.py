"""Codex 第二轮复审反例测试(R1/R2/R3/R5/R8 剩余项)。

reviews/2026-09-30-sync/REVIEW.md 的剩余问题清单,每项一个反例。
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
sys.path.insert(0, str(ROOT / "src"))

from animtrain.manifest import Entry, Manifest, sha256_file  # noqa: E402
from animtrain.validate import validate_manifest  # noqa: E402
from animtrain.run_record import RunRecord, check_record  # noqa: E402
from animtrain.preflight import check_model_dir, run_preflight  # noqa: E402


def _mk(d: Path, rel: str, text: str) -> Path:
    p = d / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


class TestR3SecondRead(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_rejected_path_not_reread(self):
        """复审 R3:被拒的越界路径不得在 split_sets/近重复阶段被再次读取。

        证据:根外放一个坏 JSON,若被读取会报 JSON 错误或读它——必须只有
        '越出根目录'一条问题,不得出现对 outside 文件的读取类问题。
        """
        _mk(self.root, "train/a.jsonl", '{"id": "t1"}\n')
        outside = self.tmp.name + "_outside"
        Path(outside).mkdir(exist_ok=True)
        (Path(outside) / "outside.jsonl").write_text("{坏 json\n", encoding="utf-8")
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(self.root / "train/a.jsonl"),
                  size=1, source="x", license="internal-generated", split="train"),
            Entry(path="../outside/outside.jsonl", sha256="", size=1,
                  source="x", license="internal-generated", split="eval")])
        r = validate_manifest(m, self.root)
        self.assertFalse(r["ok"])
        self.assertTrue(any("越出" in p for p in r["problems"]), r["problems"])
        # 不得有对越界文件的读取类问题(如 JSON 解析/哈希不一致)
        self.assertFalse(any("outside" in p and ("JSON" in p or "SHA" in p or "不一致" in p)
                             for p in r["problems"]), r["problems"])

    def test_eval_bad_json_detected(self):
        """复审 R3:坏 JSON 检查必须覆盖全部数据 split,不只 train。"""
        tr = _mk(self.root, "train/a.jsonl", '{"id": "t1"}\n')
        ev = _mk(self.root, "eval/e.jsonl", '{"id": "e1"}\n{坏 json\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(tr), size=1,
                  source="x", license="internal-generated", split="train"),
            Entry(path="eval/e.jsonl", sha256=sha256_file(ev), size=1,
                  source="x", license="internal-generated", split="eval")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("e.jsonl" in p and "JSON" in p for p in r["problems"]),
                        r["problems"])


class TestR5StrictPrecise(unittest.TestCase):
    def test_unrelated_extra_check_not_counted_as_data_gate(self):
        """复审 R5:严格模式的 data_manifest 必须真实,无关检查不能冒充。"""
        from unittest import mock
        with mock.patch("animtrain.preflight.check_gpu",
                        return_value=(True, "mock GPU")):
            r = run_preflight(None, extra_checks=[("unrelated", (True, "随便"))],
                              strict=True)
        self.assertFalse(r["ok"], "unrelated 检查不得冒充 data_manifest")
        # checks 里 data_manifest 必须是 FAIL
        dm = [c for c in r["checks"] if c["check"] == "data_manifest"]
        self.assertTrue(dm and not dm[0]["ok"], r["checks"])

    def test_zero_byte_weights_rejected(self):
        """复审 R5:0 字节 safetensors 不得在 strict 通过。"""
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            for f in ("config.json", "tokenizer_config.json", "tokenizer.json"):
                (p / f).write_text("{}", encoding="utf-8")
            (p / "model.safetensors").write_bytes(b"")
            ok, detail = check_model_dir(p, strict=True)
            self.assertFalse(ok, detail)


class TestR8MissingFile(unittest.TestCase):
    def test_manifest_path_missing_fails(self):
        """复审 R8:manifest_path 指向不存在的文件必须报,不得静默通过。"""
        r = RunRecord(run_id="x", kind="dry-run", config={"a": 1},
                      git_commit="abc", manifest_hash="f" * 64,
                      summary={"command": "x", "manifest": "data/m.json"},
                      env={"python": "3", "platform": "w", "gpu": "g"})
        problems = check_record(r, manifest_path=Path("不存在的文件.json"))
        self.assertTrue(any("manifest" in p for p in problems), problems)


class TestR1InputProtection(unittest.TestCase):
    def test_force_cannot_overwrite_plan(self):
        """复审 R1:--force 也不得覆盖任何输入文件(plan 位于输出路径时)。"""
        pool = _mk(self.tmp if hasattr(self, "tmp") else Path(tempfile.mkdtemp()),
                   "pool.jsonl", '{"id": "s1"}\n')
        # plan 文件放在 --out 目录里且与输出同名
        plan = _mk(pool.parent, "train.jsonl",
                   json.dumps({"train": ["s1"], "eval": [], "test": []},
                              ensure_ascii=False))
        r = subprocess.run(
            [str(PY), str(ROOT / "tools" / "split_data.py"),
             "--pool", str(pool), "--plan", str(plan), "--out", str(pool.parent),
             "--force"],
            capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(r.returncode, 0, "--force 覆盖了输入 plan")
        # plan 内容必须原样(还是 JSON plan,不是被 split 输出覆盖)
        self.assertIn('"train"', plan.read_text(encoding="utf-8"))


class TestR2LicenseInherit(unittest.TestCase):
    def test_split_unknown_license_not_hardcoded(self):
        """复审 R2:split 不得把未知来源硬写 internal-generated。"""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            pool = _mk(root, "pool.jsonl", '{"id": "s1"}\n')
            plan = _mk(root, "plan.json", json.dumps(
                {"train": ["s1"], "eval": [], "test": []}, ensure_ascii=False))
            out = root / "o"
            r = subprocess.run(
                [str(PY), str(ROOT / "tools" / "split_data.py"),
                 "--pool", str(pool), "--plan", str(plan), "--out", str(out)],
                capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(r.returncode, 0, r.stderr)
            m = Manifest.load(out / "split_manifest.json")
            lic = {e.path: e.license for e in m.entries}
            # 未提供许可参数时不得硬写 internal-generated(未知→空→quarantine)
            self.assertNotIn("internal-generated", lic.values(), lic)


if __name__ == "__main__":
    unittest.main()
