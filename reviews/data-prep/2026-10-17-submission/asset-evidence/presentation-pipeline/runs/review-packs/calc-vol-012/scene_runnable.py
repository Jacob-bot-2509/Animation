"""Auto-generated runnable shell for a text-only presentation candidate.

The fragment below is authored; this shell only adds the Manim import and the
Scene subclass so `manim -ql scene_runnable.py Candidate` can import it.
This file has never been executed by the pipeline.
"""
from manim import *  # noqa: F401,F403


class Candidate(Scene):
    def construct(self):
        from math import isfinite as candidate_isfinite
        if self.mobjects:
            raise ValueError('candidate_requires_dedicated_empty_canvas')
        candidate_width = config.frame_width - 1
        candidate_height = config.frame_height - 1
        if not candidate_isfinite(candidate_width) or not candidate_isfinite(candidate_height) or candidate_width <= 0 or candidate_height <= 0:
            raise ValueError('candidate_invalid_viewport')
        candidate_objects = {}
        candidate_objects[(0, 1)] = MathTex('0\\le x\\le1', font_size=22)
        candidate_objects[(0, 3)] = MathTex('0\\le y\\le\\arcsin x', font_size=22)
        candidate_objects[(1, 1)] = MathTex('y=\\arcsin x', font_size=22)
        candidate_objects[(1, 3)] = MathTex('(0,0)', font_size=22)
        candidate_objects[(1, 5)] = MathTex('(1,\\frac{\\pi}{2})', font_size=22)
        candidate_objects[(2, 1)] = MathTex('[0,1]', font_size=22)
        candidate_objects[(3, 1)] = MathTex('\\arcsin x', font_size=22)
        candidate_objects[(3, 3)] = MathTex('\\pi(\\arcsin x)^2', font_size=22)
        candidate_objects[(4, 1)] = MathTex('dV=\\pi(\\arcsin x)^2\\,dx', font_size=22)
        candidate_objects[(5, 1)] = MathTex('0<x<1', font_size=22)
        candidate_objects[(5, 3)] = MathTex("F'(x)=(\\arcsin x)^2", font_size=22)
        candidate_objects[(6, 1)] = MathTex('V=\\pi(F(1)-F(0))=\\frac{\\pi^3}{4}-2\\pi', font_size=22)
        candidate_objects[(7, 0)] = MathTex('\\frac{\\pi^3}{4}-2\\pi', font_size=22)
        candidate_objects[(0, 0)] = Text('将 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(0, 2)] = Text('、', font='Microsoft YaHei', font_size=22)
        candidate_objects[(0, 4)] = Text(' 的区域绕x轴旋转一周，求所得旋转体体积。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 0)] = Text('绘制 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 2)] = Text(' 和所给区域，端点为 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 4)] = Text(' 与 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 6)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 0)] = Text('绕x轴旋转所给区域，保留明确的横坐标范围 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 2)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 0)] = Text('展示截面圆盘的半径 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 2)] = Text(' 与面积 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 4)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 0)] = Text('写出 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 2)] = Text(' 和圆盘法积分。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 0)] = Text('在 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 2)] = Text(' 上展示分部积分及 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 4)] = Text('，端点用连续极限代入。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 0)] = Text('计算 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 2)] = Text('；有限圆盘画面不是积分的数值估计。', font='Microsoft YaHei', font_size=22)
        candidate_rows = []
        candidate_rows.append(VGroup(candidate_objects[(0, 0)], candidate_objects[(0, 1)], candidate_objects[(0, 2)], candidate_objects[(0, 3)], candidate_objects[(0, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(1, 0)], candidate_objects[(1, 1)], candidate_objects[(1, 2)], candidate_objects[(1, 3)], candidate_objects[(1, 4)], candidate_objects[(1, 5)], candidate_objects[(1, 6)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(2, 0)], candidate_objects[(2, 1)], candidate_objects[(2, 2)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(3, 0)], candidate_objects[(3, 1)], candidate_objects[(3, 2)], candidate_objects[(3, 3)], candidate_objects[(3, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(4, 0)], candidate_objects[(4, 1)], candidate_objects[(4, 2)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(5, 0)], candidate_objects[(5, 1)], candidate_objects[(5, 2)], candidate_objects[(5, 3)], candidate_objects[(5, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(6, 0)], candidate_objects[(6, 1)], candidate_objects[(6, 2)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(7, 0)]).arrange(RIGHT, buff=0))
        candidate_pages = []
        candidate_page = []
        candidate_used = 0
        for candidate_index, candidate_row in enumerate(candidate_rows):
            if not candidate_isfinite(candidate_row.width) or not candidate_isfinite(candidate_row.height) or candidate_row.width > candidate_width or candidate_row.height > candidate_height or candidate_row.height <= 0:
                raise ValueError('candidate_row_exceeds_measured_viewport')
            candidate_need = candidate_row.height + (1/4 if candidate_page else 0)
            if candidate_used + candidate_need > candidate_height:
                candidate_pages.append(candidate_page)
                candidate_page = []
                candidate_used = 0
                candidate_need = candidate_row.height
            candidate_page.append(candidate_index)
            candidate_used += candidate_need
        if candidate_page:
            candidate_pages.append(candidate_page)
        self.candidate_page_map = candidate_pages
        for candidate_indices in candidate_pages:
            candidate_group = VGroup(*[candidate_rows[i] for i in candidate_indices]).arrange(DOWN, aligned_edge=LEFT, buff=1/4)
            candidate_group.move_to(ORIGIN)
            if candidate_group.width > candidate_width or candidate_group.height > candidate_height:
                raise ValueError('candidate_page_exceeds_measured_viewport')
            self.play(FadeIn(candidate_group))
            self.wait(1)
            self.play(FadeOut(candidate_group))
            self.remove(candidate_group)
