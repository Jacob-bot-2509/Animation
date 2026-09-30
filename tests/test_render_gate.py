"""渲染/数学检查框架测试(B4:环境缺失如实 UNVERIFIED,不伪造)。"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.render_gate import (  # noqa: E402
    check_manim_available, check_sympy_available, math_check, render_check)


class TestRenderGate(unittest.TestCase):
    def test_manim_missing_is_unverified_not_pass(self):
        """B4: 环境缺失 → UNVERIFIED,不得伪装通过。"""
        with mock.patch("animtrain.render_gate.check_manim_available",
                        return_value=(False, "manim 未安装")):
            r = render_check("code", trusted=True)
        self.assertFalse(r["ok"])
        self.assertEqual(r["status"], "unverified")
        self.assertEqual(r["unverified"], ["render"])

    def test_manim_available_render_executes(self):
        """B4: 环境可用时真实执行(用假 python 输出验证执行路径)。"""
        with mock.patch("animtrain.render_gate.check_manim_available",
                        return_value=(True, "manim 可用")), \
             mock.patch("subprocess.run") as run:
            run.return_value.returncode = 0
            run.return_value.stderr = ""
            r = render_check("x = 1", trusted=True)
        self.assertTrue(r["ok"])
        self.assertEqual(r["status"], "rendered")
        # 必须走隔离子进程(禁 shell 由列表参数保证,断言命令形如 python -m manim)
        args = run.call_args.args[0]
        self.assertIn("-m", args) and self.assertIn("manim", args)

    def test_render_failure_reported(self):
        with mock.patch("animtrain.render_gate.check_manim_available",
                        return_value=(True, "ok")), \
             mock.patch("subprocess.run") as run:
            run.return_value.returncode = 1
            run.return_value.stderr = "AttributeError: no plot_curve"
            r = render_check("bad code", trusted=True)
        self.assertFalse(r["ok"])
        self.assertEqual(r["status"], "failed")
        self.assertIn("plot_curve", r["detail"])

    def test_math_missing_unverified(self):
        with mock.patch("animtrain.render_gate.check_sympy_available",
                        return_value=(False, "sympy 未安装")):
            r = math_check("x**2")
        self.assertFalse(r["ok"])
        self.assertEqual(r["unverified"], ["math"])

    def test_untrusted_code_blocked_by_default(self):
        """BR6: 隔离不足时默认拒绝执行(trusted=False)。"""
        r = render_check("任意代码", trusted=False)
        self.assertFalse(r["ok"])
        self.assertEqual(r["status"], "unverified")
        self.assertEqual(r["unverified"], ["render_isolation"])

    def test_real_environment_detection(self):
        """真实环境探测:至少返回明确的 (bool, 说明),不抛异常。"""
        for fn in (check_manim_available, check_sympy_available):
            ok, msg = fn()
            self.assertIsInstance(ok, bool)
            self.assertTrue(msg)


if __name__ == "__main__":
    unittest.main()


class TestBR2MathContract(unittest.TestCase):
    def test_true_proposition_verified(self):
        from animtrain.render_gate import math_check
        with mock.patch("animtrain.render_gate.check_sympy_available",
                        return_value=(True, "ok")):
            r = math_check("Eq(sin(x)**2 + cos(x)**2, 1)")
        self.assertTrue(r["ok"])
        self.assertEqual(r["status"], "verified")

    def test_false_proposition_disproved(self):
        """BR2: 假命题必须 disproved,不得标 verified。"""
        from animtrain.render_gate import math_check
        with mock.patch("animtrain.render_gate.check_sympy_available",
                        return_value=(True, "ok")):
            r1 = math_check("Eq(1, 2)")
            r2 = math_check("False")
        for r in (r1, r2):
            self.assertFalse(r["ok"], r)
            self.assertEqual(r["status"], "disproved")

    def test_non_boolean_rejected(self):
        """BR2 复验:数字/裸表达式不是断言,不得 verified。"""
        from animtrain.render_gate import math_check
        with mock.patch("animtrain.render_gate.check_sympy_available",
                        return_value=(True, "ok")):
            for expr in ("x", "x + 1", "1", "2", "sin(x)**2 + cos(x)**2"):
                r = math_check(expr)
                self.assertFalse(r["ok"], expr)
                self.assertEqual(r["status"], "invalid", expr)

    def test_free_symbol_unproven(self):
        """BR2: 含自由符号无法判定 → unproven,如实。"""
        from animtrain.render_gate import math_check
        with mock.patch("animtrain.render_gate.check_sympy_available",
                        return_value=(True, "ok")):
            r = math_check("x > y")  # 两个自由符号,无法判定
        self.assertFalse(r["ok"])
        self.assertEqual(r["status"], "unproven")

    def test_forbidden_patterns_rejected(self):
        """BR6: sympify 走 eval,受限模式拒绝。"""
        from animtrain.render_gate import math_check
        with mock.patch("animtrain.render_gate.check_sympy_available",
                        return_value=(True, "ok")):
            for bad in ("__import__('os')", "eval('1')", "x" * 201):
                r = math_check(bad)
                self.assertFalse(r["ok"], bad)
                self.assertEqual(r["status"], "invalid")
