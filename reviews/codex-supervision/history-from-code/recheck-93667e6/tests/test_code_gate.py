"""代码门禁测试(msg_101-4:语法/API/数学/渲染/中文-LaTeX;仪器先对照)。"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.code_gate import (  # noqa: E402
    check_api, check_code_all, check_dangerous, check_latex_cjk, check_syntax)

GOOD = '''from manim import *


class ConceptScene(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3], y_range=[-1, 1])
        curve = axes.plot(lambda x: x ** 2, color=BLUE)
        label = Text("导数", font_size=30).to_edge(UP)
        self.play(Create(axes), Create(curve), Write(label))
'''


class TestCodeGate(unittest.TestCase):
    def test_good_code_silent(self):
        self.assertEqual(check_syntax(GOOD), [])
        self.assertEqual(check_dangerous(GOOD), [])
        self.assertEqual(check_latex_cjk(GOOD), [])  # Text 中文合法(走 Pango)

    def test_syntax_error_detected(self):
        bad = "def f(:\n    pass"
        out = check_syntax(bad)
        self.assertTrue(any("语法" in x for x in out), out)

    def test_dangerous_calls_detected(self):
        for bad in ('os.system("calc")', "eval('1+1')", "exec(x)", "__import__('os')",
                    "shutil.rmtree('/')"):
            out = check_dangerous(f"x = {bad}")
            self.assertTrue(out, f"危险调用未检出: {bad}")
        # import 是语句,不能放进表达式
        out = check_dangerous("import subprocess\nimport socket")
        self.assertTrue(any("subprocess" in x for x in out), out)
        self.assertTrue(any("socket" in x for x in out), out)

    def test_chinese_in_mathtex_detected(self):
        """前项目实测教训:中文进 MathTex/Tex 必编译失败(TeX 无 CJK)。"""
        bad = 'eq = MathTex(r"\\text{斜线斜率}")'
        out = check_latex_cjk(bad)
        self.assertTrue(any("中文" in x for x in out), out)
        # 纯 ASCII 公式不报
        self.assertEqual(check_latex_cjk('eq = MathTex(r"a^2 + b^2")'), [])

    def test_chinese_in_text_allowed(self):
        """Text() 走 Pango 支持中文,不得误报。"""
        self.assertEqual(check_latex_cjk('t = Text("中文标题")'), [])

    def test_api_whitelist(self):
        whitelist = {"allowed": ["Axes", "Text", "Circle", "Scene", "BLUE",
                                 "Create", "Write"], "note": "测试白名单"}
        self.assertEqual(check_api(GOOD, whitelist), [])
        bad = "class S(Scene):\n    def construct(self):\n        t = Tree()"
        out = check_api(bad, whitelist)
        self.assertTrue(any("Tree" in x for x in out), out)

    def test_api_without_whitelist_skipped_honestly(self):
        """无白名单时不伪造检查结果:如实标注跳过。"""
        out = check_api(GOOD, None)
        self.assertEqual(out, ["api_skipped: 未提供白名单(如实跳过,不伪造)"])

    def test_full_gate_aggregates(self):
        r = check_code_all(GOOD, whitelist={"allowed": ["Axes", "Text", "Scene",
                                                        "BLUE", "Create", "Write"]})
        self.assertTrue(r["ok"], r["problems"])


if __name__ == "__main__":
    unittest.main()
