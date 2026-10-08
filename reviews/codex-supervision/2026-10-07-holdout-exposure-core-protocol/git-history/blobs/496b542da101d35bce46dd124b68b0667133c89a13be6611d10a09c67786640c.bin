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
                              ("run_snapshot", (True, "valid"))] + extra,
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


class TestAssetEvidence(unittest.TestCase):
    """B2(BR4-b 剩余):资产验收证据——缺失/损坏/未绑定/覆盖不足必须阻断。"""

    def _mk(self, d: Path, evidence: dict | None, bad_json: bool = False):
        from animtrain.manifest import Manifest
        mp = d / "manifest.json"
        Manifest(name="t", entries=[]).to_dict()
        mp.write_text('{"name": "t", "version": 1, "entries": []}',
                      encoding="utf-8")
        ep = d / "asset_evidence.json"
        if bad_json:
            ep.write_text("not json", encoding="utf-8")
        elif evidence is not None:
            import json
            ep.write_text(json.dumps(evidence, ensure_ascii=False),
                          encoding="utf-8")
        return mp

    def _sha(self, mp: Path) -> str:
        import hashlib
        return hashlib.sha256(mp.read_bytes()).hexdigest()

    def test_missing_evidence_blocks(self):
        from animtrain.preflight import check_asset_evidence
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            mp = self._mk(d, None)
            ok, detail = check_asset_evidence(mp)
            self.assertFalse(ok)
            self.assertIn("缺失", detail)

    def test_corrupt_evidence_blocks(self):
        from animtrain.preflight import check_asset_evidence
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            mp = self._mk(d, None, bad_json=True)
            ok, detail = check_asset_evidence(mp)
            self.assertFalse(ok)
            self.assertIn("损坏", detail)

    def test_unbound_evidence_blocks(self):
        from animtrain.preflight import check_asset_evidence
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            mp = self._mk(d, {"manifest_sha256": "f" * 64,
                              "n_verified_assets": 10, "n_total_records": 10})
            ok, detail = check_asset_evidence(mp)
            self.assertFalse(ok)
            self.assertIn("未绑定", detail)

    def test_insufficient_coverage_blocks(self):
        from animtrain.preflight import check_asset_evidence
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            mp = self._mk(d, None)
            import json
            ep = d / "asset_evidence.json"
            ep.write_text(json.dumps({"manifest_sha256": self._sha(mp),
                                      "n_verified_assets": 2,
                                      "n_total_records": 10}, ensure_ascii=False),
                          encoding="utf-8")
            ok, detail = check_asset_evidence(mp)
            self.assertFalse(ok)
            self.assertIn("覆盖不足", detail)

    def test_bound_full_coverage_passes(self):
        from animtrain.preflight import check_asset_evidence
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            mp = self._mk(d, None)
            import json
            ep = d / "asset_evidence.json"
            ep.write_text(json.dumps({"manifest_sha256": self._sha(mp),
                                      "n_verified_assets": 10,
                                      "n_total_records": 10}, ensure_ascii=False),
                          encoding="utf-8")
            ok, detail = check_asset_evidence(mp)
            self.assertTrue(ok, detail)
            self.assertIn("覆盖 10/10", detail)
