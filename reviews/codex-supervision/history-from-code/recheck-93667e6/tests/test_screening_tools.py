"""筛选工具静态契约测试(msg_225):tag 校验/样本冻结/空权重 provenance 失败。"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestScreeningTools(unittest.TestCase):
    def test_tag_path_escape_rejected(self):
        out = subprocess.run(
            [sys.executable, "-X", "utf8",
             str(ROOT / "tools" / "screening_probe.py"),
             "--model-dir", ".models/qwen2.5-7b-instruct",
             "--tag", "../escape"],
            capture_output=True, encoding="utf-8", errors="replace")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("tag 非法", out.stdout + out.stderr)

    def test_provenance_rejects_config_only(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "config.json").write_text("{}", encoding="utf-8")
            out = subprocess.run(
                [sys.executable, "-X", "utf8",
                 str(ROOT / "tools" / "model_provenance.py"),
                 "--model-dir", str(d), "--source", "https://x.example/y"],
                capture_output=True, encoding="utf-8", errors="replace")
            self.assertNotEqual(out.returncode, 0)
            self.assertIn("未发现已落地的权重", out.stdout + out.stderr)

    def test_provenance_detects_lfs_pointer(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "config.json").write_text("{}", encoding="utf-8")
            (d / "model-00001-of-00004.safetensors").write_text(
                "version https://git-lfs.github.com/spec/v1\noid sha256:"
                + "f" * 64 + "\nsize 100\n", encoding="ascii")
            out = subprocess.run(
                [sys.executable, "-X", "utf8",
                 str(ROOT / "tools" / "model_provenance.py"),
                 "--model-dir", str(d), "--source", "https://x.example/y"],
                capture_output=True, encoding="utf-8", errors="replace")
            self.assertNotEqual(out.returncode, 0)  # 指针未落地 → 无有效权重
            self.assertIn("LFS 指针", out.stdout + out.stderr)

    def test_sample_manifest_frozen(self):
        """样本清单冻结:同一清单复跑一致;清单不一致必须拒绝。"""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "screening_probe", ROOT / "tools" / "screening_probe.py")
        # 直接测 input_hash 的确定性
        sys.path.insert(0, str(ROOT / "tools"))
        from screening_probe import input_hash
        a = {"problem": "求 1+1。", "solution": "2"}
        self.assertEqual(input_hash(a), input_hash(dict(a)))
        b = dict(a)
        b["solution"] = "3"
        self.assertNotEqual(input_hash(a), input_hash(b))


if __name__ == "__main__":
    unittest.main()
