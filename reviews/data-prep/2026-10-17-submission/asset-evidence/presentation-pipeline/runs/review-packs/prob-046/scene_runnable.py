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
        candidate_objects[(0, 1)] = MathTex('D=[0,1]^2', font_size=22)
        candidate_objects[(2, 1)] = MathTex('D', font_size=22)
        candidate_objects[(2, 3)] = MathTex('R_0', font_size=22)
        candidate_objects[(3, 1)] = MathTex('R_1=(\\frac{1}{2},1]\\times[0,1]', font_size=22)
        candidate_objects[(3, 3)] = MathTex('\\frac{1}{2}', font_size=22)
        candidate_objects[(4, 1)] = MathTex('R_2=(\\frac{1}{4},\\frac{1}{2}]\\times[0,1]', font_size=22)
        candidate_objects[(4, 3)] = MathTex('\\frac{1}{4}', font_size=22)
        candidate_objects[(4, 5)] = MathTex('R_1', font_size=22)
        candidate_objects[(5, 1)] = MathTex('R_k', font_size=22)
        candidate_objects[(5, 3)] = MathTex('2^{-k}', font_size=22)
        candidate_objects[(7, 1)] = MathTex('S_N=1-2^{-N}', font_size=22)
        candidate_objects[(7, 3)] = MathTex('2^{-N}', font_size=22)
        candidate_objects[(8, 1)] = MathTex('1', font_size=22)
        candidate_objects[(9, 0)] = MathTex('D=R_0\\sqcup\\bigcup_{k=1}^{\\infty}R_k', font_size=22)
        candidate_objects[(9, 2)] = MathTex('S_N=1-2^{-N}', font_size=22)
        candidate_objects[(9, 4)] = MathTex('0+\\sum_{k=1}^{\\infty}2^{-k}=1', font_size=22)
        candidate_objects[(0, 0)] = Text('用单位正方形 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(0, 2)] = Text(' 的可列分割直观说明面积的可列可加性，', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 0)] = Text('并明确小矩形边界的归属。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 0)] = Text('绘制 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 2)] = Text('，明确左边界单独记为零面积集合 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 4)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 0)] = Text('画出 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 2)] = Text('，标面积 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 4)] = Text('；端点归属按定义处理。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 0)] = Text('画出 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 2)] = Text('，标面积 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 4)] = Text('，与 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 6)] = Text(' 不重叠。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 0)] = Text('继续示意有限多个 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 2)] = Text('，显示一般边界 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 4)] = Text('，', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 0)] = Text('不把共用描边误认为集合相交。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(7, 0)] = Text('显示 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(7, 2)] = Text(' 及剩余面积 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(7, 4)] = Text('，不声称有限帧已画出无限多个矩形。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(8, 0)] = Text('由等比级数极限得总面积为 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(8, 2)] = Text('；说明这是具名分割的可列可加例子。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(9, 1)] = Text('，', font='Microsoft YaHei', font_size=22)
        candidate_objects[(9, 3)] = Text('，总面积 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(9, 5)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_rows = []
        candidate_rows.append(VGroup(candidate_objects[(0, 0)], candidate_objects[(0, 1)], candidate_objects[(0, 2)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(1, 0)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(2, 0)], candidate_objects[(2, 1)], candidate_objects[(2, 2)], candidate_objects[(2, 3)], candidate_objects[(2, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(3, 0)], candidate_objects[(3, 1)], candidate_objects[(3, 2)], candidate_objects[(3, 3)], candidate_objects[(3, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(4, 0)], candidate_objects[(4, 1)], candidate_objects[(4, 2)], candidate_objects[(4, 3)], candidate_objects[(4, 4)], candidate_objects[(4, 5)], candidate_objects[(4, 6)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(5, 0)], candidate_objects[(5, 1)], candidate_objects[(5, 2)], candidate_objects[(5, 3)], candidate_objects[(5, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(6, 0)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(7, 0)], candidate_objects[(7, 1)], candidate_objects[(7, 2)], candidate_objects[(7, 3)], candidate_objects[(7, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(8, 0)], candidate_objects[(8, 1)], candidate_objects[(8, 2)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(9, 0)], candidate_objects[(9, 1)], candidate_objects[(9, 2)], candidate_objects[(9, 3)], candidate_objects[(9, 4)], candidate_objects[(9, 5)]).arrange(RIGHT, buff=0))
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
