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
        candidate_objects[(0, 1)] = MathTex('\\sum_{n=1}^{\\infty}\\frac{(-1)^n}{\\sqrt n}', font_size=22)
        candidate_objects[(1, 1)] = MathTex('n=1', font_size=22)
        candidate_objects[(1, 3)] = MathTex('-1', font_size=22)
        candidate_objects[(1, 5)] = MathTex('(-1)^n/\\sqrt n', font_size=22)
        candidate_objects[(2, 1)] = MathTex('S', font_size=22)
        candidate_objects[(2, 3)] = MathTex('|S-S_N|\\le1/\\sqrt{N+1}', font_size=22)
        candidate_objects[(3, 1)] = MathTex('1/\\sqrt n', font_size=22)
        candidate_objects[(3, 3)] = MathTex('p=\\frac{1}{2}', font_size=22)
        candidate_objects[(4, 1)] = MathTex('\\sum_{n=1}^{N}1/\\sqrt n\\ge2(\\sqrt{N+1}-1)\\to+\\infty', font_size=22)
        candidate_objects[(0, 0)] = Text('讨论级数 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(0, 2)] = Text(' 的敛散性，判定绝对收敛或条件收敛。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 0)] = Text('从 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 2)] = Text(' 的负项 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 4)] = Text(' 开始，按 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 6)] = Text(' 显示交错项。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 0)] = Text('显示奇数部分和递增、偶数部分和递减且夹住 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 2)] = Text('，并给出 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 4)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 0)] = Text('另画正项 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 2)] = Text('，标出p级数参数 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 4)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 0)] = Text('展示 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 2)] = Text('，说明发散依据是不等式而非有限折线。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 0)] = Text('对照“原级数收敛、绝对值级数发散”，判定条件收敛。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 0)] = Text('条件收敛。', font='Microsoft YaHei', font_size=22)
        candidate_rows = []
        candidate_rows.append(VGroup(candidate_objects[(0, 0)], candidate_objects[(0, 1)], candidate_objects[(0, 2)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(1, 0)], candidate_objects[(1, 1)], candidate_objects[(1, 2)], candidate_objects[(1, 3)], candidate_objects[(1, 4)], candidate_objects[(1, 5)], candidate_objects[(1, 6)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(2, 0)], candidate_objects[(2, 1)], candidate_objects[(2, 2)], candidate_objects[(2, 3)], candidate_objects[(2, 4)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(3, 0)], candidate_objects[(3, 1)], candidate_objects[(3, 2)], candidate_objects[(3, 3)], candidate_objects[(3, 4)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(4, 0)], candidate_objects[(4, 1)], candidate_objects[(4, 2)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(5, 0)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(6, 0)]).arrange(RIGHT, buff=0.12))
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
