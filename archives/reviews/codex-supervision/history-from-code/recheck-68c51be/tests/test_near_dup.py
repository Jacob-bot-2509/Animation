"""近重复检测器测试(仪器对照:必须对已知近重复对报警、对无关对静默)。

前项目纪律:检测器先过对照再用于门禁;误报会挡好数据,比漏报危险。
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.near_dup import ShingleIndex, find_near_dups, jaccard, shingles  # noqa: E402


# 阈值 0.7 是前项目用**真实长度题目**(几十到几百字符)实测校准的;
# 玩具短句(≤20 字符)5-gram 太碎,Jaccard 偏低,是已知局限(见
# test_short_text_limitation 的如实记录)。测试一律用真实长度题面。
P1 = ("某工厂生产两种产品,甲产品每件利润 3 元,乙产品每件利润 5 元。"
      "生产甲产品需要 A 材料 2 千克和 B 材料 1 千克,生产乙产品需要 "
      "A 材料 1 千克和 B 材料 3 千克。现有 A 材料 100 千克、B 材料 120 千克,"
      "问两种产品各生产多少件利润最大")
P2 = ("已知函数 f(x) = x^3 - 3x^2 + 2x + 1,求函数在区间 [-1, 2] 上的"
      "最大值与最小值,并说明在哪些点处取得")
P3 = ("在三角形 ABC 中,角 A、B、C 的对边分别为 a、b、c。已知 a = 5,"
      "b = 7,角 C = 60 度,求边 c 的长度以及三角形的面积")


class TestNearDup(unittest.TestCase):
    def test_known_near_dup_fires(self):
        """改措辞的同一题必须检出(前项目实测:仅精确重叠不够)。"""
        a = P1
        b = P1.replace("两种产品各生产多少件利润最大", "如何安排生产使利润达到最大")
        idx = ShingleIndex()
        idx.add(a, {"id": "a"})
        sim, hit = idx.max_sim(b)
        self.assertGreaterEqual(sim, 0.7, f"已知近重复未检出: sim={sim}")
        self.assertEqual(hit, {"id": "a"})

    def test_unrelated_silent(self):
        idx = ShingleIndex()
        idx.add(P1, {"id": "a"})
        sim, _ = idx.max_sim(P3)
        self.assertLess(sim, 0.7, f"无关文本被误报: sim={sim}")

    def test_number_change_still_near_dup(self):
        """只换数字:文本主体相同,应仍判近重复(完整长度题面)。"""
        a = P1
        b = P1.replace("利润 3 元", "利润 8 元").replace("100 千克", "180 千克")
        idx = ShingleIndex()
        idx.add(a, {"id": "a"})
        sim, _ = idx.max_sim(b)
        self.assertGreaterEqual(sim, 0.7, f"换数字后未检出: sim={sim}")

    def test_whitespace_cannot_evade(self):
        """加空格/换行不能绕过(归一化去空白)。"""
        a = P2
        b = "已 知 函 数 f(x) = x^3 - 3x^2 + 2x + 1,求 函 数 在 区 间 [-1,2]\n上的最大值与最小值"
        idx = ShingleIndex()
        idx.add(a, {"id": "a"})
        sim, _ = idx.max_sim(b)
        self.assertGreaterEqual(sim, 0.7, f"空白变体未检出: sim={sim}")

    def test_pool_query_api(self):
        hits = find_near_dups(
            pool_texts=[(P1, {"id": "p1"}), (P2, {"id": "p2"})],
            queries=[(P1.replace("利润最大", "利润达到最大值"), {"id": "q1"}),
                     (P3, {"id": "q2"})])
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["query"]["id"], "q1")
        self.assertEqual(hits[0]["hit"]["id"], "p1")

    def test_short_text_limitation_documented(self):
        """已知局限(如实记录,不藏):短句 5-gram 太碎,Jaccard 对措辞极敏感
        ——同一对短句,换个措辞 sim 可能 0.56(漏报),再换个措辞 0.71(检出)。
        阈值 0.7 是在真实长度题面(几十到几百字符)上校准的;
        若将来数据以短句为主,须用对照实验重校准,不许拍脑袋。"""
        a = "求解方程 x^2 + 3x + 2 = 0 的两个根"
        b = "求方程 x^2 + 3x + 2 = 0 的解"
        idx = ShingleIndex()
        idx.add(a, {"id": "a"})
        sim, _ = idx.max_sim(b)
        # 实测 0.5625:这对措辞下短句会漏报 —— 钉住局限,提醒重校准需要
        self.assertLess(sim, 0.7, f"此对短句实测低于阈值: sim={sim}")

    def test_empty_and_short_inputs(self):
        self.assertEqual(shingles(""), set())
        self.assertEqual(shingles("ab"), {"ab"})  # 短于 k 的文本整体作 shingle
        self.assertEqual(jaccard(set(), {"a"}), 0.0)
        idx = ShingleIndex()
        sim, hit = idx.max_sim("")
        self.assertEqual((sim, hit), (0.0, None))


if __name__ == "__main__":
    unittest.main()
