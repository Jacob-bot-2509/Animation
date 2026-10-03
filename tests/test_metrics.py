"""固定指标契约测试(B3):分母不缩小、失败必分类、未标注 NOT_MEASURED。"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.metrics import (  # noqa: E402
    FAILURE_TAXONOMY, SampleResult, aggregate, finalize_result, sample_hash)


class TestMetricsContract(unittest.TestCase):
    def _ok(self, sid, latency=None):
        r = SampleResult(sample_id=sid, input_hash=sample_hash("p", "s"),
                         parsed_strict=True, parsed_lenient=True)
        if latency is not None:
            r.metrics["latency_sec"] = latency
        return finalize_result(r)

    def _fail(self, sid, cls="schema_violation"):
        r = SampleResult(sample_id=sid, input_hash=sample_hash("p", "s"))
        r.failure_class = cls
        return finalize_result(r)

    def test_denominator_does_not_shrink(self):
        res = aggregate([self._ok("a", 1.0), self._ok("b", 2.0),
                         self._fail("c"), self._fail("d", "truncated")])
        self.assertEqual(res["n_samples"], 4)
        self.assertEqual(res["strict_parse_rate"], 0.5)  # 2/4,不是 2/2

    def test_failure_requires_class(self):
        r = finalize_result(SampleResult(sample_id="x",
                                         input_hash=sample_hash("p", "s")))
        self.assertEqual(r.status, "failed")
        self.assertIn(r.failure_class, FAILURE_TAXONOMY)
        self.assertTrue(r.failure_detail)

    def test_invalid_failure_class_rejected(self):
        r = SampleResult(sample_id="x", input_hash=sample_hash("p", "s"),
                         failure_class="made_up")
        with self.assertRaises(ValueError):
            finalize_result(r)

    def test_math_review_not_measured(self):
        res = aggregate([self._ok("a")])
        self.assertEqual(res["math_review_pass_rate"], "NOT_MEASURED")

    def test_latency_median_and_p95(self):
        res = aggregate([self._ok("a", i + 1.0) for i in range(10)])
        self.assertEqual(res["median_latency_sec"], 5.5)  # (5+6)/2
        self.assertEqual(res["p95_latency_sec"], 10.0)

    def test_sample_hash_deterministic_and_sensitive(self):
        self.assertEqual(sample_hash("p", "s"), sample_hash("p", "s"))
        self.assertNotEqual(sample_hash("p", "s"), sample_hash("p", "t"))


if __name__ == "__main__":
    unittest.main()
