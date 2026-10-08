"""preflight 测试(msg_101-6:GPU/模型检查清单,任何门禁失败禁止后续动作)。"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.preflight import check_gpu, check_model_dir, run_preflight  # noqa: E402


def _nvidia_ok(cmd, **kw):
    class R:
        returncode = 0
        stdout = "NVIDIA GeForce RTX 5060, 8151 MiB, 0 MiB, 7899 MiB, 0 %\n"
        stderr = ""
    return R()


def _nvidia_missing(cmd, **kw):
    raise FileNotFoundError("nvidia-smi")


class TestPreflight(unittest.TestCase):
    def test_gpu_ok(self):
        with mock.patch("subprocess.run", side_effect=_nvidia_ok):
            ok, detail = check_gpu()
        self.assertTrue(ok, detail)

    def test_gpu_missing(self):
        with mock.patch("subprocess.run", side_effect=_nvidia_missing):
            ok, detail = check_gpu()
        self.assertFalse(ok)
        self.assertIn("nvidia-smi", detail)

    def test_model_dir_checks_key_files(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            for f in ("config.json", "tokenizer_config.json", "tokenizer.json"):
                (p / f).write_text("{}", encoding="utf-8")
            ok, detail = check_model_dir(p)
            self.assertTrue(ok, detail)
            (p / "config.json").unlink()
            ok, detail = check_model_dir(p)
            self.assertFalse(ok)
            self.assertIn("config.json", detail)

    def test_any_fail_blocks_followup(self):
        """任何 FAIL → exit 1,禁止后续动作(msg_101-6)。"""
        with mock.patch("animtrain.preflight.check_gpu", return_value=(False, "x")), \
             mock.patch("animtrain.preflight.check_model_dir",
                        return_value=(True, "y")):
            r = run_preflight(model_dir=Path("."))
        self.assertFalse(r["ok"])
        self.assertEqual(r["exit_code"], 1)
        self.assertTrue(any(not c["ok"] for c in r["checks"]))

    def _ready_with(self, extra):
        with mock.patch("animtrain.preflight.check_gpu", return_value=(True, "mock")), \
             mock.patch("animtrain.preflight.check_model_dir", return_value=(True, "mock")):
            return run_preflight(
                Path("."),
                extra_checks=[("data_manifest", (True, "valid")),
                              ("run_snapshot", (True, "valid")),
                              ("asset_evidence", (True, "valid")),
                              ("freeze_gate", (True, "valid")),
                              ("near_dup_calibrated", (True, "valid")),
                              ("exec_isolation", (True, "valid"))] + extra,
                ready=True)

    def test_ready_blocks_failed_additional_gate(self):
        r = self._ready_with([("render_gate", (False, "render failed"))])
        self.assertFalse(r["ok"])
        self.assertFalse(r["ready"])
        self.assertEqual(r["exit_code"], 1)
        self.assertIn("render_gate", r["checks"][-1]["detail"])

    def test_ready_duplicate_name_cannot_hide_failure(self):
        r = self._ready_with([("data_manifest", (False, "invalid")),
                              ("data_manifest", (True, "later pass"))])
        self.assertFalse(r["ready"])
        self.assertEqual(r["exit_code"], 1)

    def test_ready_duplicate_name_cannot_hide_unverified(self):
        r = self._ready_with([
            ("math_gate", (True, "pending", {"unverified": ["math"]})),
            ("math_gate", (True, "later pass"))])
        self.assertFalse(r["ready"])
        self.assertEqual(r["exit_code"], 1)
        self.assertIn("math_gate", r["checks"][-1]["detail"])



if __name__ == "__main__":
    unittest.main()


class _AssetEvidenceHelpers(unittest.TestCase):
    """共享夹具:manifest+样本+证据构造。"""
    """B2(GS2 复修):资产验收证据必须以当前 manifest 实际样本逐条验证,
    自报数字/自报覆盖不可作为验收依据。"""

    def _mk(self, d: Path, evidence: dict | None, bad_json: bool = False,
            with_sample: bool = False):
        import json
        from animtrain.manifest import canonical_problem_hash
        mp = d / "manifest.json"
        line = ('{"id": "s1", "problem": "求 1+1 的值。", "solution": "2。", '
                '"answer": "2", "scene_spec": {"objects": ["x"], "steps": ["y"]}, '
                '"source": "x", "license": "Internal-Research-Use-Only"}')
        if with_sample:
            (d / "raw").mkdir(exist_ok=True)
            (d / "raw" / "d.jsonl").write_text(line + "\n", encoding="utf-8")
        entries = ([{"path": "raw/d.jsonl", "sha256": "", "size": len(line) + 1,
                     "source": "x", "license": "Internal-Research-Use-Only",
                     "split": "raw"}] if with_sample else [])
        mp.write_text(json.dumps({"name": "t", "version": 1, "entries": entries},
                                 ensure_ascii=False), encoding="utf-8")
        ep = d / "asset_evidence.json"
        if bad_json:
            ep.write_text("not json", encoding="utf-8")
        elif evidence is not None:
            ep.write_text(json.dumps(evidence, ensure_ascii=False),
                          encoding="utf-8")
        return mp, line

    def _sha(self, mp: Path) -> str:
        import hashlib
        return hashlib.sha256(mp.read_bytes()).hexdigest()

    def test_missing_evidence_blocks(self):
        from animtrain.preflight import check_asset_evidence
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            mp, _ = self._mk(d, None, with_sample=True)
            ok, detail = check_asset_evidence(mp)
            self.assertFalse(ok)
            self.assertIn("缺失", detail)

    def test_corrupt_evidence_blocks(self):
        from animtrain.preflight import check_asset_evidence
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            mp, _ = self._mk(d, None, bad_json=True, with_sample=True)
            ok, detail = check_asset_evidence(mp)
            self.assertFalse(ok)
            self.assertIn("损坏", detail)

    def test_unbound_evidence_blocks(self):
        from animtrain.preflight import check_asset_evidence
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            mp, _ = self._mk(d, {"manifest_sha256": "f" * 64,
                                 "records": {}, "n_verified_assets": 0,
                                 "n_total_records": 0}, with_sample=True)
            ok, detail = check_asset_evidence(mp)
            self.assertFalse(ok)
            self.assertIn("未绑定", detail)

    def test_self_reported_numbers_alone_rejected(self):
        """GS2:自报 1/1 无逐条证据 → 拒绝。"""
        from animtrain.preflight import check_asset_evidence
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            mp, _ = self._mk(d, None, with_sample=True)
            import json
            (d / "asset_evidence.json").write_text(json.dumps(
                {"manifest_sha256": self._sha(mp),
                 "n_verified_assets": 1, "n_total_records": 1},
                ensure_ascii=False), encoding="utf-8")
            ok, detail = check_asset_evidence(mp)
            self.assertFalse(ok)
            self.assertIn("逐条记录", detail)

    def _evidence(self, mp: Path, line: str, output=None):
        import hashlib
        return {"manifest_sha256": self._sha(mp),
                "n_total_records": 1, "n_verified_assets": 1,
                "records": {"s1": {
                    "input_sha256": hashlib.sha256(
                        line.strip().encode("utf-8")).hexdigest(),
                    "output": output or {},
                    "math": "verified", "render": "rendered", "semantic": "verified"}}}

    def test_per_record_evidence_passes(self):
        from animtrain.preflight import check_asset_evidence
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            mp, line = self._mk(d, None, with_sample=True)
            import hashlib
            artifact = d / "render-out.png"
            from PIL import Image
            Image.new("RGB", (2, 2), "blue").save(artifact)
            out = {"path": str(artifact.relative_to(d)),
                   "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
                   "size": artifact.stat().st_size}
            import json
            (d / "asset_evidence.json").write_text(json.dumps(
                self._evidence(mp, line, output=out), ensure_ascii=False),
                encoding="utf-8")
            ok, detail = check_asset_evidence(mp)
            self.assertTrue(ok, detail)
            self.assertIn("1/1", detail)

    def test_record_input_hash_mismatch_rejected(self):
        from animtrain.preflight import check_asset_evidence
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            mp, _line = self._mk(d, None, with_sample=True)
            import json
            ev = self._evidence(mp, _line)
            ev["records"]["s1"]["input_sha256"] = "f" * 64
            (d / "asset_evidence.json").write_text(json.dumps(ev, ensure_ascii=False))
            ok, detail = check_asset_evidence(mp)
            self.assertFalse(ok)
            self.assertIn("不一致", detail)

    def test_missing_per_record_evidence_rejected(self):
        from animtrain.preflight import check_asset_evidence
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            mp, _line = self._mk(d, None, with_sample=True)
            import json
            ev = self._evidence(mp, _line)
            ev["records"] = {"s2": ev["records"]["s1"]}
            (d / "asset_evidence.json").write_text(json.dumps(ev, ensure_ascii=False))
            ok, detail = check_asset_evidence(mp)
            self.assertFalse(ok)
            self.assertIn("s1", detail)


class TestAssetEvidenceMsg216(_AssetEvidenceHelpers):
    """msg_216:产物必须绑定真实 artifact 文件;占位字符串不得通过。"""

    def test_no_artifact_placeholder_rejected(self):
        from animtrain.preflight import check_asset_evidence
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            mp, _line = self._mk(d, None, with_sample=True)
            ev = self._evidence(mp, _line, output={})
            import json
            (d / "asset_evidence.json").write_text(json.dumps(ev, ensure_ascii=False))
            ok, detail = check_asset_evidence(mp)
            self.assertFalse(ok)
            self.assertIn("产物记录", detail)

    def test_artifact_file_missing_rejected(self):
        from animtrain.preflight import check_asset_evidence
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            mp, _line = self._mk(d, None, with_sample=True)
            ev = self._evidence(mp, _line, output={
                "path": "nonexistent.svg", "sha256": "f" * 64, "size": 1})
            import json
            (d / "asset_evidence.json").write_text(json.dumps(ev, ensure_ascii=False))
            ok, detail = check_asset_evidence(mp)
            self.assertFalse(ok)
            self.assertIn("不存在", detail)

    def test_artifact_hash_mismatch_rejected(self):
        from animtrain.preflight import check_asset_evidence
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            mp, _line = self._mk(d, None, with_sample=True)
            artifact = d / "out.svg"
            artifact.write_text("<svg/>", encoding="utf-8")
            ev = self._evidence(mp, _line, output={
                "path": "out.svg", "sha256": "f" * 64, "size": len(b"<svg/>")})
            import json
            (d / "asset_evidence.json").write_text(json.dumps(ev, ensure_ascii=False))
            ok, detail = check_asset_evidence(mp)
            self.assertFalse(ok)
            self.assertIn("不一致", detail)
