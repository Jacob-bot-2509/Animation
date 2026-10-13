"""标注成对校准回归：精确边界、排除不确定、完整网格和缺失值。"""
import importlib.util
import json
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("b5_pairs", ROOT / "tools/b5_calibrate.py")
b5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b5)


def pair(a, b, label="重复"):
    return {"a": "a", "b": "b", "text_a": a, "text_b": b,
            "label": label, "jaccard": 1}


class TestPairwiseCalibration(unittest.TestCase):
    def test_recomputes_score_and_uses_exact_boundary(self):
        rows = [pair("abcdef", "abcdeg")]
        self.assertEqual(b5.evaluate_pairs(rows, Fraction(1, 3))["tp"], 1)
        self.assertEqual(b5.evaluate_pairs(rows, Fraction(33334, 100000))["fn"], 1)
        self.assertEqual(b5.evaluate_pairs(rows, Fraction(1, 2))["tp"], 0)

    def test_separable_sample_and_full_grid(self):
        report = b5.build_report({"pairs": [
            pair("abcdef", "abcdef"),
            pair("abcdef", "uvwxyz", "不重复"),
            pair("abcdef", "abcdef", "不确定")]})
        self.assertTrue(report["calibration"]["calibrated"])
        self.assertEqual(report["calibration"]["threshold"], "3/10")
        self.assertEqual(len(report["grid"]), 11)
        self.assertEqual(report["uncertain_pairs"], 1)
        self.assertTrue(all(row["pos"] == row["neg"] == 1 for row in report["grid"]))
        self.assertEqual(report["grid"][0]["precision"], "1")

    def test_inseparable_sample_has_no_fake_measurement(self):
        report = b5.build_report({"pairs": [pair("abcdef", "abcdef"),
            pair("abcdef", "abcdef", "不重复")]})
        self.assertFalse(report["calibration"]["calibrated"])
        self.assertIsNone(report["calibration"]["threshold"])
        self.assertIsNone(report["calibration"]["tp"])
        self.assertEqual(report["grid"][0]["precision"], "1/2")

    def test_empty_predictions_display_undefined(self):
        report = b5.build_report({"pairs": [
            pair("abcdef", "uvwxyz"), pair("abcdef", "uvwxyz", "不重复")]})
        self.assertIsNone(report["grid"][0]["precision"])
        text = b5.render_markdown(report)
        self.assertIn("未定义", text)
        self.assertNotIn("None", text)

    def test_unknown_labels_rejected(self):
        with self.assertRaises(ValueError):
            b5.build_report({"pairs": [pair("abcdef", "abcdef", "typo")]})

    def test_actual_sample_counts_and_exact_output(self):
        annotation = json.loads((ROOT / "data/b5-annotation-set/b5-annotation-set.json")
                                .read_text(encoding="utf-8"))
        report = b5.build_report(annotation)
        self.assertEqual((report["pos_pairs"], report["neg_pairs"],
                          report["uncertain_pairs"]), (11, 37, 2))
        half = next(row for row in report["grid"] if row["threshold"] == "1/2")
        self.assertEqual((half["tp"], half["fp"], half["fn"], half["tn"]), (9, 3, 2, 34))
        self.assertEqual((half["precision"], half["recall"], half["fpr"]),
                         ("3/4", "9/11", "3/37"))
        self.assertFalse(report["calibration"]["calibrated"])
        def assert_exact(value):
            if isinstance(value, dict):
                for item in value.values(): assert_exact(item)
            elif isinstance(value, list):
                for item in value: assert_exact(item)
            else: self.assertNotIsInstance(value, float)
        assert_exact(report)
