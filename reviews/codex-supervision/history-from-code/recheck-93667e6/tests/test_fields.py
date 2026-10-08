"""字段映射校验测试(msg_101-3:核心字段必须与真实项目对应,不得丢失)。"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.fields import check_fields  # noqa: E402


class TestFields(unittest.TestCase):
    def test_all_required_present(self):
        rows = [{"id": "a", "problem": "题", "solution": "解", "answer": "42"},
                {"sample_id": "b", "problem": "题2", "solution": "解2", "answer": "3"}]
        bad = check_fields(rows, required=["problem", "solution", "answer"])
        self.assertEqual(bad, [])

    def test_missing_field_detected_with_sample_id(self):
        """失败保留原始 sample_id 与原因(msg_101-3)。"""
        rows = [{"id": "a", "problem": "题", "answer": "42"},
                {"sample_id": "b", "problem": "题2", "solution": "解2", "answer": "3"}]
        bad = check_fields(rows, required=["problem", "solution", "answer"])
        self.assertEqual(len(bad), 1)
        self.assertEqual(bad[0]["sample_id"], "a")
        self.assertIn("solution", bad[0]["missing"])

    def test_optional_field_not_required(self):
        """scene_spec 按数据类型可配:不在 required 列表就不查。"""
        rows = [{"id": "a", "problem": "题", "solution": "解", "answer": "42"}]
        bad = check_fields(rows, required=["problem", "solution", "answer"])
        self.assertEqual(bad, [])

    def test_empty_value_counts_as_missing(self):
        """空字符串/空值算缺失,不算存在。"""
        rows = [{"id": "a", "problem": "题", "solution": "", "answer": "42"}]
        bad = check_fields(rows, required=["problem", "solution", "answer"])
        self.assertEqual(len(bad), 1)
        self.assertIn("solution", bad[0]["missing"])


if __name__ == "__main__":
    unittest.main()
