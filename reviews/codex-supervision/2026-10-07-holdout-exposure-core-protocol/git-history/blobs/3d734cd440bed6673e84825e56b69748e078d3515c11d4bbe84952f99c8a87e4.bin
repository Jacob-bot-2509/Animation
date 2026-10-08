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
        """An existing rejected file must never reach any reader."""
        from unittest import mock
        import animtrain.validate as validation

        allowed_root = self.root / "scope"
        train = _mk(allowed_root, "train/a.jsonl", '{"id":"t1"}\n')
        outside = _mk(self.root, "outside.jsonl", '{"id":"outside"}\n')
        self.assertEqual((allowed_root / "../outside.jsonl").resolve(),
                         outside.resolve())
        m = Manifest(name="t", entries=[
            Entry(path="train/a.jsonl", sha256=sha256_file(train),
                  size=train.stat().st_size, source="test",
                  license="internal-generated", split="train"),
            Entry(path="../outside.jsonl", sha256=sha256_file(outside),
                  size=outside.stat().st_size, source="test",
                  license="internal-generated", split="eval")])
        original_read = Path.read_text
        original_open = Path.open

        def guarded_read(path, *args, **kwargs):
            self.assertNotEqual(path.resolve(), outside.resolve())
            return original_read(path, *args, **kwargs)

        def guarded_open(path, *args, **kwargs):
            self.assertNotEqual(path.resolve(), outside.resolve())
            return original_open(path, *args, **kwargs)

        with mock.patch.object(Path, "read_text", guarded_read), \
             mock.patch.object(Path, "open", guarded_open):
            r = validation.validate_manifest(m, allowed_root)
        self.assertFalse(r["ok"])
        self.assertEqual(len(r["problems"]), 1)
        self.assertIn("../outside.jsonl", r["problems"][0])

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
        """Use separate pool/out directories so only the input guard can stop it."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            pool = _mk(root, "input/pool.jsonl", '{"id":"s1"}\n')
            plan = _mk(root, "output/train.jsonl", json.dumps(
                {"train": ["s1"], "eval": [], "test": []}))
            before = plan.read_bytes()
            self.assertNotEqual(pool.parent.resolve(), plan.parent.resolve())
            r = subprocess.run(
                [str(PY), str(ROOT / "tools" / "split_data.py"),
                 "--pool", str(pool), "--plan", str(plan),
                 "--out", str(plan.parent), "--force"],
                capture_output=True, text=True, encoding="utf-8")
            self.assertNotEqual(r.returncode, 0)
            self.assertEqual(plan.read_bytes(), before)
            self.assertFalse((plan.parent / "split_manifest.json").exists())


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
