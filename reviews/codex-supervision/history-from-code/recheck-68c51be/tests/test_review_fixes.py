"""Codex 审查修复测试(R1/R2/R3/R4/R7/R8/R5/R6 的反例,测试先行)。

probe_results.json 复现的缺陷,每项一个反例;修复后这些必须全部转 FAIL。
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
from animtrain.fields import check_fields, check_jsonl  # noqa: E402
from animtrain.run_record import RunRecord, check_record  # noqa: E402
from animtrain.code_gate import check_code_all  # noqa: E402
from animtrain.preflight import run_preflight  # noqa: E402


def _mk(d: Path, rel: str, text: str) -> Path:
    p = d / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


class TestR1WriteProtection(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_split_refuses_to_overwrite_pool(self):
        """反例 R1: pool=train.jsonl, out=pool.parent 会原地覆盖池子。"""
        pool = _mk(self.root, "d/pool.jsonl", '{"id": "s1"}\n{"id": "s2"}\n')
        plan = _mk(self.root, "plan.json", json.dumps(
            {"train": ["s1", "s2"], "eval": [], "test": []}, ensure_ascii=False))
        out = pool.parent  # 攻击:输出到池子所在目录
        r = subprocess.run(
            [str(PY), str(ROOT / "tools" / "split_data.py"),
             "--pool", str(pool), "--plan", str(plan), "--out", str(out), "--allow-empty"],
            capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(r.returncode, 0, "应拒绝覆盖池子所在目录的输出")
        # 池子必须原样保留两条
        self.assertEqual(len(pool.read_text(encoding="utf-8").splitlines()), 2)

    def test_split_refuses_existing_output(self):
        pool = _mk(self.root, "d/pool.jsonl", '{"id": "s1"}\n')
        plan = _mk(self.root, "plan.json", json.dumps(
            {"train": ["s1"], "eval": [], "test": []}, ensure_ascii=False))
        out = _mk(self.root, "o/train.jsonl", "旧内容\n")  # 已有输出
        r = subprocess.run(
            [str(PY), str(ROOT / "tools" / "split_data.py"),
             "--pool", str(pool), "--plan", str(plan), "--out", str(out.parent)],
            capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(r.returncode, 0, "应拒绝覆盖已存在的输出")
        self.assertIn("旧内容", out.read_text(encoding="utf-8"))

    def test_run_id_path_guard(self):
        """反例 R1: run_id 含路径分隔符可穿越 runs/ 目录。"""
        for bad in ("../evil", "a/b", "..\\x", "a b"):
            r = RunRecord(run_id=bad, kind="dry-run", config={"a": 1},
                          git_commit="abc", manifest_hash="f" * 64,
                          summary={"command": "x"})
            self.assertTrue(any("run_id" in p for p in check_record(r)),
                            f"run_id={bad!r} 未拦截")


class TestR2SplitManifest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_split_manifest_loads_as_manifest(self):
        """反例 R2: split_manifest 必须能被 Manifest.load 直接读。"""
        pool = _mk(self.root, "d/pool.jsonl", '{"id": "s1"}\n{"id": "s2"}\n')
        plan = _mk(self.root, "plan.json", json.dumps(
            {"train": ["s1"], "eval": ["s2"], "test": []}, ensure_ascii=False))
        out = self.root / "o"
        r = subprocess.run(
            [str(PY), str(ROOT / "tools" / "split_data.py"),
             "--pool", str(pool), "--plan", str(plan), "--out", str(out), "--allow-empty"],
            capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)
        m = Manifest.load(out / "split_manifest.json")
        splits = {e.path: e.split for e in m.entries}
        self.assertEqual(splits.get("train.jsonl"), "train")
        self.assertEqual(splits.get("eval.jsonl"), "eval")


class TestR3ManifestStrict(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_missing_source_or_sha_fails(self):
        """反例 R3: 来源或 SHA256 为空不得 ok=true。"""
        p = _mk(self.root, "train/a.jsonl", '{"id": "t1"}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256="", size=1, source="",
                  license="internal-generated", split="train")])
        r = validate_manifest(m, self.root)
        self.assertFalse(r["ok"], "来源/SHA 为空仍通过")
        self.assertTrue(any("SHA256" in x or "来源" in x
                            for x in r["problems"] + r["quarantines"]), r)

    def test_bad_json_in_train_detected(self):
        """反例 R3: 坏 JSON train 行必须检出,不是静默通过。"""
        p = _mk(self.root, "train/a.jsonl", '{"id": "t1"}\n{坏 json\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(p), size=1,
                  source="x", license="internal-generated", split="train")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("JSON" in x or "解析" in x for x in r["problems"]), r)

    def test_path_escape_blocked(self):
        """反例 R3: entry.path 含 ../ 越出根目录必须拦截。"""
        _mk(self.root, "train/a.jsonl", '{"id": "t1"}\n')
        m = Manifest(name="t", entries=[
            Entry(path="../outside.jsonl", sha256="", size=1, source="x",
                  license="internal-generated", split="train")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("越出" in x or "根目录" in x for x in r["problems"]), r)


class TestR4CrossSet(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_eval_test_same_id_detected(self):
        """反例 R4: eval 与 test 彼此同 ID 不同内容,此前可通过。"""
        ev = _mk(self.root, "eval/e.jsonl", '{"id": "dup", "problem": "评测版"}\n')
        te = _mk(self.root, "test/t.jsonl", '{"id": "dup", "problem": "测试版"}\n')
        tr = _mk(self.root, "train/a.jsonl", '{"id": "t1"}\n')
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(tr), size=1,
                  source="x", license="internal-generated", split="train"),
            Entry(path="eval/e.jsonl", sha256=sha256_file(ev), size=1,
                  source="x", license="internal-generated", split="eval"),
            Entry(path="test/t.jsonl", sha256=sha256_file(te), size=1,
                  source="x", license="internal-generated", split="test")])
        r = validate_manifest(m, self.root)
        self.assertTrue(any("eval" in x and "test" in x or "ID 重叠" in x
                            for x in r["problems"]), r["problems"])


class TestR7Fields(unittest.TestCase):
    def test_answer_zero_not_missing(self):
        """反例 R7: answer=0 是合法值,不得判缺失。"""
        bad = check_fields([{"id": "zero", "problem": "p", "solution": "s",
                             "answer": 0}], required=["problem", "solution", "answer"])
        self.assertEqual(bad, [])

    def test_true_source_line(self):
        """反例 R7: 第二行起必须报真实行号,不是恒为 1。"""
        p = Path(self.tmp.name) if hasattr(self, "tmp") else None
        import tempfile as _t
        with _t.TemporaryDirectory() as d:
            f = Path(d) / "x.jsonl"
            f.write_text('{"id": "ok", "problem": "p", "solution": "s", "answer": "1"}\n'
                         '{"id": "bad"}\n', encoding="utf-8")
            bad = check_jsonl(f, required=["problem", "solution", "answer"])
            self.assertEqual(len(bad), 1)
            self.assertEqual(bad[0]["line"], 2, f"行号应为 2,实际 {bad[0]['line']}")
            self.assertEqual(bad[0]["sample_id"], "bad")


class TestR8RunRecordStrict(unittest.TestCase):
    def test_missing_manifest_env_fails(self):
        """反例 R8: 缺 manifest 路径/空 env 必须 fail-fast。"""
        r = RunRecord(run_id="x", kind="dry-run", config={"a": 1},
                      git_commit="abc", manifest_hash="f" * 64,
                      summary={"command": "x"})
        problems = check_record(r)
        self.assertTrue(any("manifest" in p for p in problems), problems)
        self.assertTrue(any("env" in p for p in problems), problems)


class TestR6Alias(unittest.TestCase):
    def test_import_alias_detected(self):
        """反例 R6: import os as operating; operating.system(...) 必须检出。"""
        code = ('import os as operating\n'
                'operating.system("never executed")\n')
        r = check_code_all(code, whitelist={"allowed": ["Text"]})
        self.assertTrue(any("operating" in p or "os" in p for p in r["problems"]),
                        r["problems"])


class TestR5PreflightStrict(unittest.TestCase):
    def test_mock_gpu_only_not_strict_pass(self):
        """反例 R5: 只有 mock GPU 成功时,严格模式不得通过。"""
        from unittest import mock
        with mock.patch("animtrain.preflight.check_gpu",
                        return_value=(True, "mock GPU")):
            r = run_preflight(None, strict=True)
        self.assertFalse(r["ok"], "严格模式下仅 mock GPU 不应通过")
        self.assertEqual(r["exit_code"], 1)

    def test_model_without_weights_rejected_strict(self):
        """反例 R5: 只有空 JSON 无权重的模型目录,严格模式必须拒绝。"""
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            for f in ("config.json", "tokenizer_config.json", "tokenizer.json"):
                (p / f).write_text("{}", encoding="utf-8")
            from animtrain.preflight import check_model_dir
            ok, detail = check_model_dir(p, strict=True)
            self.assertFalse(ok, detail)
            self.assertIn("权重", detail)


if __name__ == "__main__":
    unittest.main()
