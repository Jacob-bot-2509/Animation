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


class TestTableStyles(unittest.TestCase):
    @staticmethod
    def table(headers):
        return "<table><thead><tr>" + "".join("<th>" + h + "</th>" for h in headers) + "</tr></thead></table>"

    def test_multiple_grids_receive_grid_style(self):
        grid = self.table(["阈值", "TP", "FP", "FN", "TN", "精确率", "召回率", "误报率"])
        rendered = renderer.style_tables(grid + grid)
        self.assertEqual(rendered.count('class="grid"'), 2)

    def test_styles_follow_headers_even_when_reordered(self):
        revision = self.table(["对", "原标注", "改判", "理由"])
        uncertain = self.table(["题目A(考点)", "题目B(考点)", "规则预测"])
        pairs = self.table(["J5(文字)", "标注", "题目A(考点)", "题目B(考点)"])
        for table, kind in ((revision, "revision"), (uncertain, "uncertain"), (pairs, "pairs")):
            self.assertIn(f'class="{kind}"', renderer.style_tables(table))
        output = renderer.style_tables(revision + uncertain + pairs)
        self.assertLess(output.index('class="revision"'), output.index('class="pairs"'))

    def test_unrecognized_table_does_not_inherit_pair_column_widths(self):
        self.assertIn('class="generic"', renderer.style_tables(self.table(["项目", "说明"])))
