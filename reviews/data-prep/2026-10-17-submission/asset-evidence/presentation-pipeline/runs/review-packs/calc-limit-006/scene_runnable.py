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
        candidate_objects[(0, 1)] = MathTex('\\lim_{x\\to0}\\frac{\\sin x}{x}', font_size=22)
        candidate_objects[(1, 1)] = MathTex('O,A', font_size=22)
        candidate_objects[(1, 3)] = MathTex('x=\\frac{\\pi}{4}', font_size=22)
        candidate_objects[(2, 1)] = MathTex('B=(\\cos x,\\sin x)', font_size=22)
        candidate_objects[(2, 3)] = MathTex('D=(\\cos x,0)', font_size=22)
        candidate_objects[(2, 5)] = MathTex('\\triangle OAB', font_size=22)
        candidate_objects[(2, 7)] = MathTex('\\frac{\\sin x}{2}', font_size=22)
        candidate_objects[(3, 1)] = MathTex('OAB', font_size=22)
        candidate_objects[(3, 3)] = MathTex('x', font_size=22)
        candidate_objects[(3, 5)] = MathTex('\\frac{x}{2}', font_size=22)
        candidate_objects[(4, 1)] = MathTex('u=1', font_size=22)
        candidate_objects[(4, 3)] = MathTex('C=(1,\\tan x)', font_size=22)
        candidate_objects[(4, 5)] = MathTex('\\triangle OAC', font_size=22)
        candidate_objects[(4, 7)] = MathTex('\\frac{\\tan x}{2}', font_size=22)
        candidate_objects[(5, 1)] = MathTex('\\frac{\\sin x}{2}<\\frac{x}{2}<\\frac{\\tan x}{2}', font_size=22)
        candidate_objects[(5, 3)] = MathTex('\\cos x<\\frac{\\sin x}{x}<1', font_size=22)
        candidate_objects[(6, 1)] = MathTex('x', font_size=22)
        candidate_objects[(6, 3)] = MathTex('0', font_size=22)
        candidate_objects[(6, 5)] = MathTex('x=0', font_size=22)
        candidate_objects[(8, 1)] = MathTex('\\lim_{x\\to0}\\frac{\\sin x}{x}=1', font_size=22)
        candidate_objects[(9, 0)] = MathTex('1', font_size=22)
        candidate_objects[(0, 0)] = Text('求极限 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(0, 2)] = Text('（角度采用弧度）。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 0)] = Text('绘制单位圆和坐标轴，标出 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 2)] = Text('；以精确初始角 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 4)] = Text(' 绘制射线。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 0)] = Text('标出 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 2)] = Text(' 和 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 4)] = Text('，填充 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 6)] = Text('，标注面积 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 8)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 0)] = Text('填充扇形 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 2)] = Text('，标注弧度角 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 4)] = Text(' 和面积 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 6)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 0)] = Text('作切线 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 2)] = Text('，标出 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 4)] = Text('，填充 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 6)] = Text('，标注面积 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 8)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 0)] = Text('展示严格面积比较 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 2)] = Text(' 及 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 4)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 0)] = Text('令 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 2)] = Text(' 从正侧趋于 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 4)] = Text('；图形只示意过程，不在 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 6)] = Text(' 计算比值，', font='Microsoft YaHei', font_size=22)
        candidate_objects[(7, 0)] = Text('极限判断依据精确不等式。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(8, 0)] = Text('显示右极限的夹逼推导、偶函数等式和左极限，得 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(8, 2)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_rows = []
        candidate_rows.append(VGroup(candidate_objects[(0, 0)], candidate_objects[(0, 1)], candidate_objects[(0, 2)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(1, 0)], candidate_objects[(1, 1)], candidate_objects[(1, 2)], candidate_objects[(1, 3)], candidate_objects[(1, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(2, 0)], candidate_objects[(2, 1)], candidate_objects[(2, 2)], candidate_objects[(2, 3)], candidate_objects[(2, 4)], candidate_objects[(2, 5)], candidate_objects[(2, 6)], candidate_objects[(2, 7)], candidate_objects[(2, 8)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(3, 0)], candidate_objects[(3, 1)], candidate_objects[(3, 2)], candidate_objects[(3, 3)], candidate_objects[(3, 4)], candidate_objects[(3, 5)], candidate_objects[(3, 6)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(4, 0)], candidate_objects[(4, 1)], candidate_objects[(4, 2)], candidate_objects[(4, 3)], candidate_objects[(4, 4)], candidate_objects[(4, 5)], candidate_objects[(4, 6)], candidate_objects[(4, 7)], candidate_objects[(4, 8)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(5, 0)], candidate_objects[(5, 1)], candidate_objects[(5, 2)], candidate_objects[(5, 3)], candidate_objects[(5, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(6, 0)], candidate_objects[(6, 1)], candidate_objects[(6, 2)], candidate_objects[(6, 3)], candidate_objects[(6, 4)], candidate_objects[(6, 5)], candidate_objects[(6, 6)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(7, 0)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(8, 0)], candidate_objects[(8, 1)], candidate_objects[(8, 2)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(9, 0)]).arrange(RIGHT, buff=0))
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
