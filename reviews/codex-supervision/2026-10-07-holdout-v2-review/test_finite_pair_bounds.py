import itertools
import unittest
from fractions import Fraction
from finite_pair_bounds import interval, probability, allocate, unrank, final_bounds

class ExactBoundsTests(unittest.TestCase):
    def test_exact_tail_noncoverage_exhaustively(self):
        alpha = Fraction(1, 20)
        for N in range(1, 9):
            for m in range(N + 1):
                bounds = {x: interval(N, m, x, alpha) for x in range(m + 1)}
                for K in range(N + 1):
                    p = sum((probability(N, m, K, x) for x in range(m + 1)), Fraction())
                    self.assertEqual(p, 1)
                    lm = sum((probability(N, m, K, x) for x, (L, U) in bounds.items()
                              if K < L), Fraction())
                    um = sum((probability(N, m, K, x) for x, (L, U) in bounds.items()
                              if K > U), Fraction())
                    self.assertLessEqual(lm, alpha)
                    self.assertLessEqual(um, alpha)

    def test_zero_sample_and_census(self):
        self.assertEqual(interval(391, 0, 0, Fraction(1, 160)), (0, 391))
        for N in range(1, 20):
            for x in range(N + 1):
                self.assertEqual(interval(N, N, x, Fraction(1, 160)), (x, x))

    def test_combination_unranking_all_small_cases(self):
        for N in range(9):
            for m in range(N + 1):
                expected = list(itertools.combinations(range(N), m))
                self.assertEqual([unrank(N, m, r) for r in range(len(expected))], expected)

    def test_allocation_capacity_sum_and_coverage(self):
        for caps in itertools.product(range(1, 5), repeat=3):
            for B in range(sum(caps) + 3):
                values = allocate(caps, B)
                self.assertEqual(sum(values), min(B, sum(caps)))
                self.assertTrue(all(0 <= m <= n for m, n in zip(values, caps)))
                if B >= len(caps):
                    self.assertTrue(all(m > 0 for m in values))

    def test_census_exact_ratios_and_joint_alpha(self):
        row = {"N": 300, "m": 300, "counts": {"FP": 0, "TN": 240, "TP": 57, "FN": 3, "U": 0}}
        result = final_bounds({"P1": [row], "P2": [row]})
        self.assertEqual(result["alpha_per_tail"], Fraction(1, 320))
        self.assertEqual(1 - 8 * result["H"] * result["alpha_per_tail"], Fraction(19, 20))
        for frame in result["frames"].values():
            self.assertEqual(frame["FPR_upper"], 0)
            self.assertEqual(frame["Recall_lower"], Fraction(19, 20))
        self.assertTrue(result["all_statistical_criteria_met"])
        self.assertFalse(result["gate_accepted"])

    def test_empty_classes_are_not_passes(self):
        row = {"N": 5, "m": 5, "counts": {"FP": 0, "TN": 0, "TP": 0, "FN": 0, "U": 5}}
        r = final_bounds({"P1": [row], "P2": [row]})
        self.assertFalse(r["all_statistical_criteria_met"])
        self.assertIsNone(r["frames"]["P1"]["FPR_upper"])

    def test_unsampled_strata_not_silently_omitted(self):
        row = {"N": 300, "m": 300, "counts": {"FP": 0, "TN": 240, "TP": 60, "FN": 0, "U": 0}}
        empty = {"N": 300, "m": 0, "counts": dict.fromkeys(("FP","TN","TP","FN","U"), 0)}
        r = final_bounds({"P1": [row, empty], "P2": [row]})
        self.assertFalse(r["all_statistical_criteria_met"])
        self.assertIsNone(r["frames"]["P1"]["HT_point_estimates"])
        self.assertGreater(r["frames"]["P1"]["FPR_upper"], Fraction(1, 100))

    def test_missing_positives_not_synthesized(self):
        row = {"N": 300, "m": 300, "counts": {"FP": 0, "TN": 300, "TP": 0, "FN": 0, "U": 0}}
        r = final_bounds({"P1": [row], "P2": [row]})
        self.assertIsNone(r["frames"]["P1"]["Recall_lower"])
        self.assertFalse(r["all_statistical_criteria_met"])

    def test_input_rejections(self):
        for bad in [(5, 6, 0), (5, 2, 3), (True, 0, 0)]:
            with self.assertRaises(ValueError):
                interval(*bad, Fraction(1, 20))
        with self.assertRaises(ValueError):
            interval(5, 2, 1, float(Fraction(1,20)))
        with self.assertRaises(ValueError):
            unrank(5, 2, 10)
        with self.assertRaises(ValueError):
            final_bounds({"P1": [{"N": 2, "m": 1, "counts": {"FP":1}}]})

if __name__ == "__main__":
    unittest.main()
