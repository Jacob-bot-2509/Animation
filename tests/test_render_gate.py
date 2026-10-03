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
             mock.patch.object(sys, "platform", "linux"), \
             mock.patch("subprocess.Popen") as popen:
            proc = mock.MagicMock()
            proc.communicate.return_value = ("", "")
            proc.returncode = 0
            popen.return_value = proc
            r = render_check("x = 1", trusted=True)
        self.assertTrue(r["ok"])
        self.assertEqual(r["status"], "rendered")
        # 必须走隔离子进程(禁 shell 由列表参数保证,断言命令形如 python -m manim)
        args = popen.call_args.args[0]
        self.assertIn("-m", args) and self.assertIn("manim", args)

    def test_render_failure_reported(self):
        with mock.patch("animtrain.render_gate.check_manim_available",
                        return_value=(True, "ok")), \
             mock.patch.object(sys, "platform", "linux"), \
             mock.patch("subprocess.Popen") as popen:
            proc = mock.MagicMock()
            proc.communicate.return_value = ("", "AttributeError: no plot_curve")
            proc.returncode = 1
            popen.return_value = proc
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


class TestRenderGateRealMathTex(unittest.TestCase):
    """msg_141:聚焦测试 —— 真实 MathTex 正常路径与非法失败路径。"""

    def test_math_tex_real_render(self):
        """真实渲染:MathTex ASCII 场景通过(regression:dvisvgm cwd 空格崩溃)。"""
        from animtrain.render_gate import render_check
        code = ('from manim import *\n\n\n'
                'class ConceptScene(Scene):\n'
                '    def construct(self):\n'
                '        eq = MathTex(r"x^2")\n'
                '        self.add(eq)\n'
                '        self.wait(0.2)\n')
        r = render_check(code, trusted=True)
        self.assertTrue(r["ok"], r["detail"])
        self.assertEqual(r["status"], "rendered")

    def test_bad_api_fails(self):
        """非法 API(不存在的类)必须 failed,不得渲染成功。"""
        from animtrain.render_gate import render_check
        code = ('from manim import *\n\n\n'
                'class ConceptScene(Scene):\n'
                '    def construct(self):\n'
                '        t = Tree()\n')
        r = render_check(code, trusted=True)
        self.assertFalse(r["ok"])
        self.assertEqual(r["status"], "failed")

    def test_syntax_error_fails(self):
        from animtrain.render_gate import render_check
        r = render_check("def f(:\n    pass", trusted=True)
        self.assertFalse(r["ok"])
        self.assertEqual(r["status"], "failed")


class TestB4Hardening(unittest.TestCase):
    """B4:不可信数学输入受限解析 + 环境脱敏 + 隔离状态如实。"""

    def test_safe_parse_valid_assertion(self):
        from animtrain.render_gate import _safe_parse
        import sympy
        r = _safe_parse("Eq(2 + 2, 4)")
        self.assertTrue(sympy.simplify(r) is sympy.S.true)

    def test_safe_parse_whitelisted_function(self):
        from animtrain.render_gate import _safe_parse
        _safe_parse("sin(0) < 1")  # 白名单函数可用,不抛

    def test_exploit_dunder_rejected(self):
        from animtrain.render_gate import _safe_parse
        with self.assertRaises(ValueError):
            _safe_parse("__import__('os').system('dir')")

    def test_exploit_attribute_rejected(self):
        from animtrain.render_gate import _safe_parse
        with self.assertRaises(ValueError):
            _safe_parse("os.system('dir')")

    def test_exploit_import_rejected(self):
        from animtrain.render_gate import _safe_parse
        with self.assertRaises(ValueError):
            _safe_parse("import os")

    def test_math_check_exploit_invalid(self):
        from animtrain.render_gate import math_check
        r = math_check("__import__('os').system('dir')")
        self.assertEqual(r["status"], "invalid")
        self.assertFalse(r["ok"])

    def test_env_sanitized_keeps_path(self):
        import os
        from unittest import mock
        from animtrain.render_gate import _sanitized_env
        fake = {"PATH": "C:/x", "SYSTEMROOT": "C:/Windows",
                "GITHUB_TOKEN": "secret", "MY_API_KEY": "sk-123"}
        with mock.patch.dict(os.environ, fake, clear=True):
            env = _sanitized_env()
        self.assertIn("PATH", env)
        self.assertNotIn("GITHUB_TOKEN", env)
        self.assertNotIn("MY_API_KEY", env)

    def test_isolation_state_honest(self):
        from animtrain.render_gate import _isolation_state
        st = _isolation_state()
        # Windows 下 job object 可用时内存上限已实施;不可用则如实 None
        if sys.platform == "win32":
            self.assertIn(st["memory_limit_mb"], (None, 2048))
        else:
            self.assertIsNone(st["memory_limit_mb"])
        # B4(2026-10-03):网络隔离已实施(socket shim+死代理,如实标注 OS 级边界)
        self.assertTrue(st["network_isolation"])
        self.assertEqual(st["fs_isolation"], "cwd_only")  # fs 仍未完整隔离

    def test_check_exec_isolation_blocks(self):
        from animtrain.preflight import check_exec_isolation
        ok, detail = check_exec_isolation()
        if sys.platform == "win32":
            # Windows 下 job+网络隔离齐备 → 验收通过;反之如实阻断
            from animtrain.render_gate import _isolation_state
            mem_ok = _isolation_state()["memory_limit_mb"] is not None
            self.assertEqual(ok, mem_ok)
            if not ok:
                self.assertIn("隔离未实施", detail)
        else:
            # 非 Windows:内存 job 不可用 → 必须阻断
            self.assertFalse(ok)
            self.assertIn("隔离未实施", detail)
