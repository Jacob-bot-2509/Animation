"""训练前准备静态校验(msg_190/191):配置模板契约 + train-only manifest。
只做静态检查,不训练、不下载、不安装。"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.manifest import sha256_file  # noqa: E402

REQUIRED_FIELDS = ["task", "dataset_manifest", "split", "seed", "model",
                   "method", "max_seq_length", "learning_rate", "batch_size",
                   "gradient_accumulation_steps", "epochs", "eval_strategy",
                   "output_dir"]
FORBIDDEN_KEYS = ["api_key", "token", "password", "secret", "credential"]


class TestTrainConfigTemplate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p = ROOT / "train_config.template.json"
        cls.tpl = json.loads(p.read_text(encoding="utf-8"))

    def test_json_valid_and_fields_present(self):
        for f in REQUIRED_FIELDS:
            self.assertIn(f, self.tpl, f"模板缺字段 {f}")

    def test_split_is_train(self):
        self.assertEqual(self.tpl["split"], "train")

    def test_unknown_hyperparams_marked_tbd(self):
        """未知超参数必须 TBD,不得伪造已验证数值。"""
        for f in ["seed", "max_seq_length", "learning_rate", "batch_size",
                  "gradient_accumulation_steps", "epochs", "eval_strategy"]:
            self.assertTrue(str(self.tpl[f]).startswith("TBD"),
                            f"{f} 必须为 TBD(允许带括号说明)")
        self.assertIn("Qwen2.5-7B-Instruct", self.tpl["model"]["name"])
        self.assertIn("待下载/实测/批准", self.tpl["model"]["name"])

    def test_no_credentials(self):
        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    self.assertFalse(any(bad in k.lower() for bad in FORBIDDEN_KEYS),
                                     f"疑似凭据键 {k}")
                    walk(v)
            elif isinstance(o, list):
                for x in o:
                    walk(x)
        walk(self.tpl)

    def test_task_does_not_claim_manim_code(self):
        self.assertIn("scene_spec", self.tpl["task"])
        self.assertIn("不默认训练 Manim code", self.tpl["task"])


class TestManifestTrain(unittest.TestCase):
    def test_all_entries_train_and_sha256_match(self):
        p = ROOT / "data/v1/manifest-train.json"
        m = json.loads(p.read_text(encoding="utf-8"))
        self.assertEqual(len(m["entries"]), 4)
        for e in m["entries"]:
            self.assertEqual(e["split"], "train")
            f = ROOT / "data/v1" / e["path"]
            self.assertEqual(e["sha256"], sha256_file(f),
                             f"{e['path']} 哈希与登记不一致")
            self.assertIn("provisional", e.get("notes", ""),
                          "train-only 条目必须标注 provisional/candidate 语义")

    def test_raw_manifest_kept_intact(self):
        """原始 manifest(raw 口径)与 train-only 清单并存,不互相覆盖。"""
        raw = json.loads((ROOT / "data/v1/manifest.json")
                         .read_text(encoding="utf-8"))
        self.assertTrue(all(e["split"] == "raw" for e in raw["entries"]))


class TestPrepDocs(unittest.TestCase):
    def test_train_prep_plan_exists_with_gates(self):
        text = (ROOT / "TRAIN_PREP_PLAN.md").read_text(encoding="utf-8")
        for phrase in ["不启动训练", "provisional train", "PREPARED/NOT READY",
                       "用户明确批准", "TBD", "8GB"]:
            self.assertIn(phrase, text, f"TRAIN_PREP_PLAN.md 缺关键说明 {phrase}")


if __name__ == "__main__":
    unittest.main()
