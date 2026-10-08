"""阈值校准框架测试(B5:对照集方法验证,不达标如实 UNCALIBRATED)。"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.calibrate import calibrate_threshold, evaluate_at  # noqa: E402

P = ("某工厂生产两种产品,甲产品每件利润3元,乙产品每件利润5元。生产甲产品"
     "需要A材料2千克和B材料1千克,生产乙产品需要A材料1千克和B材料3千克。"
     "现有A材料100千克、B材料120千克,问两种产品各生产多少件利润最大。")
Q = ("在三角形ABC中,角A、B、C的对边分别为a、b、c。已知a=5,b=7,角C=60度,"
     "求边c的长度以及三角形的面积。")


class TestCalibrate(unittest.TestCase):
    def test_clear_separation_calibrates(self):
        """对照集可分离时:校准成功且指标自洽。"""
        pool = [P, Q]
        pos = [P.replace("利润最大", "利润达到最大值"),  # 与 P 近重复
               Q.replace("求边c", "求第三条边")]          # 与 Q 近重复
        neg = ["证明根号二不是有理数,并说明反证法的步骤。",
               "某数列的前n项和为Sn=n^2,求其通项公式。"]
        rep = calibrate_threshold(pool, pos, neg)
        self.assertTrue(rep.calibrated, rep.note)
        self.assertEqual(rep.tp, 2)
        self.assertEqual(rep.tn, 2)

    def test_impossible_targets_uncorrected(self):
        """对照集不可分离(neg 与 pool 同样相似)时:如实 UNCALIBRATED。"""
        pool = [P]
        pos = [P.replace("利润最大", "利润达到最大值")]
        # neg 与 pool 的相似度与 pos 一样高 —— 任何阈值都无法
        # 同时召回 pos 又排除 neg(recall=1 与 fpr=0 不可兼得)
        neg = [P.replace("利润最大", "利润取得最大值")]
        rep = calibrate_threshold(pool, pos, neg, min_recall=1.0, max_fpr=0.0)
        self.assertFalse(rep.calibrated)
        self.assertIn("UNCALIBRATED", rep.note)

    def test_metrics_consistent(self):
        """四项指标互洽:tp+fn=pos 数,fp+tn=neg 数。"""
        r = evaluate_at([P, Q], [P], [Q], threshold=0.7)
        self.assertEqual(r["tp"] + r["fn"], 1)
        self.assertEqual(r["fp"] + r["tn"], 1)


if __name__ == "__main__":
    unittest.main()
