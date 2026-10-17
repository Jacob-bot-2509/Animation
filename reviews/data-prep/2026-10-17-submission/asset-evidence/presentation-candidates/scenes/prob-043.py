        from math import isfinite as candidate_isfinite
        if self.mobjects:
            raise ValueError('candidate_requires_dedicated_empty_canvas')
        candidate_width = config.frame_width - 1
        candidate_height = config.frame_height - 1
        if not candidate_isfinite(candidate_width) or not candidate_isfinite(candidate_height) or candidate_width <= 0 or candidate_height <= 0:
            raise ValueError('candidate_invalid_viewport')
        candidate_objects = {}
        candidate_objects[(2, 1)] = MathTex('U[0,1]', font_size=22)
        candidate_objects[(3, 1)] = MathTex('\\bar X_n', font_size=22)
        candidate_objects[(3, 3)] = MathTex('Z_n=\\sqrt n(\\bar X_n-\\mu)/\\sigma', font_size=22)
        candidate_objects[(4, 1)] = MathTex('f_2(t)=4t', font_size=22)
        candidate_objects[(4, 3)] = MathTex('4(1-t)', font_size=22)
        candidate_objects[(5, 1)] = MathTex('n=2,5,10,30', font_size=22)
        candidate_objects[(7, 1)] = MathTex('\\frac{1}{12n}', font_size=22)
        candidate_objects[(7, 3)] = MathTex('N(0,1)', font_size=22)
        candidate_objects[(8, 1)] = MathTex('n=30', font_size=22)
        candidate_objects[(10, 0)] = MathTex('\\frac{\\sqrt n(\\bar X_n-\\mu)}{\\sigma}\\xrightarrow{d}N(0,1)', font_size=22)
        candidate_objects[(10, 2)] = MathTex('\\bar X_n\\xrightarrow{P}\\mu', font_size=22)
        candidate_objects[(10, 4)] = MathTex('\\operatorname{Var}(\\bar X_n)=\\frac{\\sigma^2}{n}', font_size=22)
        candidate_objects[(10, 6)] = MathTex('0<\\sigma^2<\\infty', font_size=22)
        candidate_objects[(0, 0)] = Text('说明独立同分布且具有正的有限方差时，中心极限定理描述的标准化样本', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 0)] = Text('均值极限，并区别未标准化均值的变化。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 0)] = Text('声明一般定理的独立同分布和正有限方差条件；演示例单独固定为 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 2)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 0)] = Text('分别展示 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 2)] = Text(' 和 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 4)] = Text('，不可混用两种横轴。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 0)] = Text('用 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 2)] = Text(' 或 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 4)] = Text(' 的分段式画均值密度，说明均值是和的缩放。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 0)] = Text('比较 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 2)] = Text(' 时的材料；实际密度须据推导，经验直方图须据真实样本，不', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 0)] = Text('虚构数据。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(7, 0)] = Text('展示未标准化均值方差 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(7, 2)] = Text(' 趋零；标准化后才讨论趋向固定的 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(7, 4)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(8, 0)] = Text('正态曲线只作比较，不宣称 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(8, 2)] = Text(' 必然重合；用CLT极限与切比雪夫界', font='Microsoft YaHei', font_size=22)
        candidate_objects[(9, 0)] = Text('说明结论。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(10, 1)] = Text('，', font='Microsoft YaHei', font_size=22)
        candidate_objects[(10, 3)] = Text('，', font='Microsoft YaHei', font_size=22)
        candidate_objects[(10, 5)] = Text('，其中 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(10, 7)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_rows = []
        candidate_rows.append(VGroup(candidate_objects[(0, 0)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(1, 0)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(2, 0)], candidate_objects[(2, 1)], candidate_objects[(2, 2)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(3, 0)], candidate_objects[(3, 1)], candidate_objects[(3, 2)], candidate_objects[(3, 3)], candidate_objects[(3, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(4, 0)], candidate_objects[(4, 1)], candidate_objects[(4, 2)], candidate_objects[(4, 3)], candidate_objects[(4, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(5, 0)], candidate_objects[(5, 1)], candidate_objects[(5, 2)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(6, 0)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(7, 0)], candidate_objects[(7, 1)], candidate_objects[(7, 2)], candidate_objects[(7, 3)], candidate_objects[(7, 4)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(8, 0)], candidate_objects[(8, 1)], candidate_objects[(8, 2)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(9, 0)]).arrange(RIGHT, buff=0))
        candidate_rows.append(VGroup(candidate_objects[(10, 0)], candidate_objects[(10, 1)], candidate_objects[(10, 2)], candidate_objects[(10, 3)], candidate_objects[(10, 4)], candidate_objects[(10, 5)], candidate_objects[(10, 6)], candidate_objects[(10, 7)]).arrange(RIGHT, buff=0))
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
