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
        candidate_objects[(2, 1)] = MathTex('A', font_size=22)
        candidate_objects[(3, 1)] = MathTex('k+1', font_size=22)
        candidate_objects[(3, 3)] = MathTex('365-k', font_size=22)
        candidate_objects[(5, 1)] = MathTex('P(\\bar A)=\\prod_{k=0}^{29}\\frac{365-k}{365}', font_size=22)
        candidate_objects[(5, 3)] = MathTex('\\frac{365!}{335!\\,365^{30}}', font_size=22)
        candidate_objects[(6, 1)] = MathTex('P(A)=1-P(\\bar A)', font_size=22)
        candidate_objects[(8, 0)] = MathTex('1-\\prod_{k=0}^{29}\\frac{365-k}{365}=1-\\frac{365!}{335!\\,365^{30}}', font_size=22)
        candidate_objects[(0, 0)] = Text('房间里随机聚集30个人，生日在365天中等可能且相互独立。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 0)] = Text('求至少有两人生日相同的概率。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 0)] = Text('明确事件 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 2)] = Text(' 为至少两人同生日，其对立事件为30人生日全不同。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 0)] = Text('按序标注第 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 2)] = Text(' 人在全不同条件下的可选格数 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 4)] = Text('；这是条件计数，', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 0)] = Text('不是所有实际样本必须无碰撞。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 0)] = Text('逐项展示 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 2)] = Text('，并给出阶乘式 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 4)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 0)] = Text('以 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 2)] = Text(' 显示精确答案，允许事件中出现多对或多人碰撞，', font='Microsoft YaHei', font_size=22)
        candidate_objects[(7, 0)] = Text('不显示近似小数。', font='Microsoft YaHei', font_size=22)
        candidate_rows = []
        candidate_rows.append(VGroup(candidate_objects[(0, 0)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(1, 0)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(2, 0)], candidate_objects[(2, 1)], candidate_objects[(2, 2)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(3, 0)], candidate_objects[(3, 1)], candidate_objects[(3, 2)], candidate_objects[(3, 3)], candidate_objects[(3, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(4, 0)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(5, 0)], candidate_objects[(5, 1)], candidate_objects[(5, 2)], candidate_objects[(5, 3)], candidate_objects[(5, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(6, 0)], candidate_objects[(6, 1)], candidate_objects[(6, 2)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(7, 0)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(8, 0)]).arrange(RIGHT, buff=0))
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
