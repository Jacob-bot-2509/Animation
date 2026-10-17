        from math import isfinite as candidate_isfinite
        if self.mobjects:
            raise ValueError('candidate_requires_dedicated_empty_canvas')
        candidate_width = config.frame_width - 1
        candidate_height = config.frame_height - 1
        if not candidate_isfinite(candidate_width) or not candidate_isfinite(candidate_height) or candidate_width <= 0 or candidate_height <= 0:
            raise ValueError('candidate_invalid_viewport')
        candidate_objects = {}
        candidate_objects[(0, 1)] = MathTex('\\sum_{n=1}^{\\infty}\\frac{x^n}{n^2}', font_size=22)
        candidate_objects[(0, 3)] = MathTex('[-1,1]', font_size=22)
        candidate_objects[(1, 1)] = MathTex('[-1,1]', font_size=22)
        candidate_objects[(1, 3)] = MathTex('y=\\pm\\frac{\\pi^2}{6}', font_size=22)
        candidate_objects[(2, 1)] = MathTex('N=1,3,5,20', font_size=22)
        candidate_objects[(3, 1)] = MathTex('|x^n/n^2|\\le1/n^2', font_size=22)
        candidate_objects[(4, 1)] = MathTex('S_{200}', font_size=22)
        candidate_objects[(4, 3)] = MathTex('S_{200}\\pm E_{200}', font_size=22)
        candidate_objects[(6, 1)] = MathTex('\\|f-S_N\\|_\\infty=E_N', font_size=22)
        candidate_objects[(6, 3)] = MathTex('E_N\\to0', font_size=22)
        candidate_objects[(7, 1)] = MathTex('\\|f-S_N\\|_\\infty=\\frac{\\pi^2}{6}-\\sum_{n=1}^{N}\\frac{1}{n^2}\\to0', font_size=22)
        candidate_objects[(0, 0)] = Text('讨论 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(0, 2)] = Text(' 在 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(0, 4)] = Text(' 上是否一致收敛。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 0)] = Text('绘出 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 2)] = Text(' 和界直线 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 4)] = Text('；有界本身不是一致收敛证明。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 0)] = Text('按精确公式展示 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 2)] = Text(' 的部分和多项式。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 0)] = Text('展示M判别法 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 2)] = Text(' 与收敛控制级数。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 0)] = Text('若显示 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 2)] = Text('，明确标为有限多项式，并用 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 4)] = Text(' 夹住和函数，', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 0)] = Text('不画成已知精确的极限曲线。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 0)] = Text('给出精确统一余项等式 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 2)] = Text('，由 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 4)] = Text(' 完成证明。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(7, 0)] = Text('一致收敛，且 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(7, 2)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_rows = []
        candidate_rows.append(VGroup(candidate_objects[(0, 0)], candidate_objects[(0, 1)], candidate_objects[(0, 2)], candidate_objects[(0, 3)], candidate_objects[(0, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(1, 0)], candidate_objects[(1, 1)], candidate_objects[(1, 2)], candidate_objects[(1, 3)], candidate_objects[(1, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(2, 0)], candidate_objects[(2, 1)], candidate_objects[(2, 2)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(3, 0)], candidate_objects[(3, 1)], candidate_objects[(3, 2)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(4, 0)], candidate_objects[(4, 1)], candidate_objects[(4, 2)], candidate_objects[(4, 3)], candidate_objects[(4, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(5, 0)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(6, 0)], candidate_objects[(6, 1)], candidate_objects[(6, 2)], candidate_objects[(6, 3)], candidate_objects[(6, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(7, 0)], candidate_objects[(7, 1)], candidate_objects[(7, 2)]).arrange(RIGHT, buff=0))
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
