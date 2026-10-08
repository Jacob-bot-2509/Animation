"""B5 v3回归：固定签名规则、真实题文、缺失记录和精确分数对照。"""
import importlib.util
import json
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("b5_pairs", ROOT / "tools/b5_calibrate.py")
b5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b5)


def fixture_pair(a, b, records, label="重复"):
    return {"a": a, "b": b, "text_a": records[a]["problem"],
            "text_b": records[b]["problem"], "label": label, "jaccard": 1}


def record(text, category="数学分析", sub=""):
    return {"category": category, "problem": text, "sub_category": sub}


class TestPairwiseCalibration(unittest.TestCase):
    def test_exact_5gram_boundary_ignores_saved_similarity(self):
        prepared = b5._prepare_pair({"a": "a", "b": "b", "text_a": "abcdef",
                                   "text_b": "abcdeg", "label": "重复", "jaccard": 1})
        self.assertEqual(prepared["jaccard"], "1/3")
        self.assertEqual(b5._evaluate([prepared], Fraction(1, 3), "jaccard")["tp"], 1)
        self.assertEqual(b5._evaluate([prepared], Fraction(33334, 100000),
                                     "jaccard")["fn"], 1)

    def test_separable_sample_uses_fixed_signature_threshold(self):
        records = {"a": record("求极限甲"), "b": record("求极限乙"),
                   "c": record("求不定积分甲")}
        annotation = {"pairs": [fixture_pair("a", "b", records),
                                fixture_pair("a", "c", records, "不重复"),
                                fixture_pair("b", "c", records, "不确定")]}
        report = b5.build_report(annotation, records)
        self.assertTrue(report["calibration"]["calibrated"])
        self.assertEqual(report["calibration"]["threshold"], "1")
        self.assertEqual(len(report["grid_kp"]), 3)
        self.assertEqual(len(report["grid_5gram_contrast"]), 11)
        self.assertEqual(report["uncertain_pairs"], 1)
        self.assertTrue(all(row["pos"] == row["neg"] == 1 for row in report["grid_kp"]))

    def test_lower_threshold_cannot_calibrate_different_signatures(self):
        records = {"a": record("求极限甲"), "b": record("求不定积分甲"),
                   "c": record("求特征值", "高等代数")}
        report = b5.build_report({"pairs": [fixture_pair("a", "b", records),
                      fixture_pair("a", "c", records, "不重复")]}, records)
        diagnostic = report["grid_kp"][1]
        self.assertEqual((diagnostic["recall"], diagnostic["fpr"]), ("1", "0"))
        self.assertFalse(report["calibration"]["calibrated"])
        self.assertIsNone(report["calibration"]["threshold"])
        self.assertIsNone(report["calibration"]["tp"])
        self.assertEqual(len(report["mismatches"]), 1)

    def test_conflicting_labels_do_not_manufacture_zero_counts(self):
        records = {"a": record("求极限甲"), "b": record("求极限乙")}
        report = b5.build_report({"pairs": [fixture_pair("a", "b", records),
                    fixture_pair("a", "b", records, "不重复")]}, records)
        self.assertFalse(report["calibration"]["calibrated"])
        self.assertIsNone(report["calibration"]["tp"])
        self.assertEqual(report["grid_kp"][-1]["precision"], "1/2")

    def test_unknown_labels_rejected(self):
        with self.assertRaises(ValueError):
            b5.build_report({"pairs": [{"a": "a", "b": "b", "text_a": "a",
                            "text_b": "b", "label": "typo"}]}, {})

    def test_missing_uncertain_record_is_a_validation_error(self):
        annotation = {"pairs": [{"a": "missing", "b": "also_missing",
                      "text_a": "x", "text_b": "y", "label": "不确定"}]}
        with self.assertRaisesRegex(ValueError, "无结构化记录"):
            b5.build_report(annotation, {})

    def test_stale_annotation_text_is_rejected(self):
        records = {"a": record("求极限甲"), "b": record("求极限乙")}
        pair = fixture_pair("a", "b", records)
        pair["text_a"] = "旧题文"
        with self.assertRaisesRegex(ValueError, "题文与结构化记录不一致"):
            b5.build_report({"pairs": [pair]}, records)

    def test_missing_metadata_cannot_be_a_common_signature(self):
        for rec in ({}, record("题目", category=""), record(""), record("未知题型")):
            with self.subTest(rec=rec), self.assertRaises(ValueError):
                b5.kp_signature(rec)

    def test_general_determinant_is_not_tridiagonal(self):
        self.assertEqual(b5.classify_kp(record("求行列式的值。", "高等代数")), "行列式计算")
        self.assertEqual(b5.classify_kp(record("求三对角行列式的值。", "高等代数")),
                         "三对角行列式")

    def test_scalar_ode_is_not_a_system(self):
        self.assertEqual(b5.classify_kp(record("求微分方程 y'=y 的通解。")), "常微分方程")
        self.assertEqual(b5.classify_kp(record("求微分方程组的通解。")), "微分方程组")

    def test_fields_in_signature_do_not_collide(self):
        tokens = b5.kp_tokens(record("求极限", category="极限计算"))
        self.assertEqual(tokens, {("category", "极限计算"), ("kind", "极限计算")})
        self.assertEqual(len(tokens), 2)

    def test_current_sample_counts_and_exact_output(self):
        annotation = json.loads((ROOT / "data/b5-annotation-set/b5-annotation-set.json")
                                .read_text(encoding="utf-8"))
        report = b5.build_report(annotation)
        self.assertEqual((report["pos_pairs"], report["neg_pairs"],
                          report["uncertain_pairs"]), (17, 31, 2))
        self.assertEqual((report["calibration"]["tp"], report["calibration"]["fp"],
                          report["calibration"]["fn"], report["calibration"]["tn"]),
                         (17, 0, 0, 31))
        self.assertEqual(report["mismatches"], [])
        self.assertEqual(report["calibration"]["threshold"], "1")
        def assert_exact(value):
            if isinstance(value, dict):
                for item in value.values(): assert_exact(item)
            elif isinstance(value, list):
                for item in value: assert_exact(item)
            else: self.assertNotIsInstance(value, float)
        assert_exact(report)


class TestMathTableEscaping(unittest.TestCase):
    def test_absolute_value_bars_keep_tex_meaning(self):
        math = r"$P(|X-50|\ge10)$"
        escaped = b5._md_escape("求 " + math + "；文字 A|B")
        self.assertIn(math, escaped)
        self.assertIn(r"A\|B", escaped)
        self.assertNotIn(r"\|X", escaped)

    def test_display_math_bars_are_preserved(self):
        math = "$$|x|\n+|y|$$"
        self.assertIn(math, b5._md_escape("文本|列 " + math))
