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
        candidate_objects[(2, 1)] = MathTex('y=\\frac{1}{2}', font_size=22)
        candidate_objects[(2, 3)] = MathTex('\\varepsilon>0', font_size=22)
        candidate_objects[(3, 1)] = MathTex('F_n=\\frac{\\#\\text{正面}}{n}', font_size=22)
        candidate_objects[(6, 1)] = MathTex('E(F_n)=\\frac{1}{2}', font_size=22)
        candidate_objects[(6, 3)] = MathTex('\\operatorname{Var}(F_n)=\\frac{1}{4n}', font_size=22)
        candidate_objects[(7, 1)] = MathTex('n\\to\\infty', font_size=22)
        candidate_objects[(8, 0)] = MathTex('F_n\\xrightarrow{P}\\frac{1}{2}', font_size=22)
        candidate_objects[(8, 2)] = MathTex('P(|F_n-\\frac{1}{2}|\\ge\\varepsilon)\\le\\frac{1}{4n\\varepsilon^2}', font_size=22)
        candidate_objects[(8, 4)] = MathTex('\\varepsilon>0', font_size=22)
        candidate_objects[(0, 0)] = Text('在独立重复抛掷公平硬币的条件下，', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 0)] = Text('用伯努利大数定律说明正面频率随试验次数增加的收敛意义。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 0)] = Text('声明独立公平抛掷，绘出 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 2)] = Text(' 及固定 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 4)] = Text(' 的阈值带。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 0)] = Text('有限样本的每个点必须按真实序列计算 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 2)] = Text('；', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 0)] = Text('没有实际序列时只显示公式，不伪造试验数据。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 0)] = Text('说明有限轨迹可以反复离开或进入阈值带，误差不必单调减小。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 0)] = Text('展示 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 2)] = Text('、', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 4)] = Text(' 和切比雪夫不等式。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(7, 0)] = Text('令 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(7, 2)] = Text('，由概率上界趋于零得依概率收敛；有限图像仅作示意。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(8, 1)] = Text('，且 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(8, 3)] = Text('（', font='Microsoft YaHei', font_size=22)
        candidate_objects[(8, 5)] = Text('）。', font='Microsoft YaHei', font_size=22)
        candidate_rows = []
        candidate_rows.append(VGroup(candidate_objects[(0, 0)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(1, 0)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(2, 0)], candidate_objects[(2, 1)], candidate_objects[(2, 2)], candidate_objects[(2, 3)], candidate_objects[(2, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(3, 0)], candidate_objects[(3, 1)], candidate_objects[(3, 2)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(4, 0)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(5, 0)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(6, 0)], candidate_objects[(6, 1)], candidate_objects[(6, 2)], candidate_objects[(6, 3)], candidate_objects[(6, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(7, 0)], candidate_objects[(7, 1)], candidate_objects[(7, 2)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(8, 0)], candidate_objects[(8, 1)], candidate_objects[(8, 2)], candidate_objects[(8, 3)], candidate_objects[(8, 4)], candidate_objects[(8, 5)]).arrange(RIGHT, buff=0))
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
