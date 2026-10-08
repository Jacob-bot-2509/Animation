"""MathJax检查只统计实际错误节点，样式定义不得触发误报。"""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
spec = importlib.util.spec_from_file_location("b5_renderer", ROOT / "tools/render_b5_report.py")
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


class TestMathNodes(unittest.TestCase):
    def test_error_css_is_not_an_error_node(self):
        self.assertEqual(renderer.math_errors(
            '<style>g[data-mml-node="merror"] {fill:red}</style>'), 0)

    def test_actual_math_error_fails(self):
        self.assertEqual(renderer.math_errors('<g data-mml-node="merror"></g>'), 1)

    def test_error_attribute_fails(self):
        self.assertEqual(renderer.math_errors(
            '<mjx-container data-mjx-error="unknown command"></mjx-container>'), 1)
