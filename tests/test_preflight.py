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
