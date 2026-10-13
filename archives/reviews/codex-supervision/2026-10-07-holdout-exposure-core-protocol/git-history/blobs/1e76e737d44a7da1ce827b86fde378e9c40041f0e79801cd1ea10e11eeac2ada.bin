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
            r = render_check("code")
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
            r = render_check("x = 1")
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
            r = render_check("bad code")
        self.assertFalse(r["ok"])
        self.assertEqual(r["status"], "failed")
        self.assertIn("plot_curve", r["detail"])

    def test_math_missing_unverified(self):
        with mock.patch("animtrain.render_gate.check_sympy_available",
                        return_value=(False, "sympy 未安装")):
            r = math_check("x**2")
        self.assertFalse(r["ok"])
        self.assertEqual(r["unverified"], ["math"])

    def test_real_environment_detection(self):
        """真实环境探测:至少返回明确的 (bool, 说明),不抛异常。"""
        for fn in (check_manim_available, check_sympy_available):
            ok, msg = fn()
            self.assertIsInstance(ok, bool)
            self.assertTrue(msg)


if __name__ == "__main__":
    unittest.main()
