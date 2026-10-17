        from math import isfinite as candidate_isfinite
        if self.mobjects:
            raise ValueError('candidate_requires_dedicated_empty_canvas')
        candidate_width = config.frame_width - 1
        candidate_height = config.frame_height - 1
        if not candidate_isfinite(candidate_width) or not candidate_isfinite(candidate_height) or candidate_width <= 0 or candidate_height <= 0:
            raise ValueError('candidate_invalid_viewport')
        candidate_objects = {}
        candidate_objects[(0, 1)] = MathTex('\\iint_D(1-x^2-y^2)\\,dx\\,dy', font_size=22)
        candidate_objects[(0, 3)] = MathTex('D=\\{(x,y):x^2+y^2\\le1\\}', font_size=22)
        candidate_objects[(1, 1)] = MathTex('D:x^2+y^2\\le1', font_size=22)
        candidate_objects[(1, 3)] = MathTex('z=0', font_size=22)
        candidate_objects[(1, 5)] = MathTex('z=1-x^2-y^2', font_size=22)
        candidate_objects[(2, 1)] = MathTex('1', font_size=22)
        candidate_objects[(2, 3)] = MathTex('0', font_size=22)
        candidate_objects[(3, 1)] = MathTex('(1-\\xi_i^2-\\eta_i^2)\\Delta A_i', font_size=22)
        candidate_objects[(6, 1)] = MathTex('r\\,dr\\,d\\theta', font_size=22)
        candidate_objects[(7, 1)] = MathTex('2\\pi[\\frac{r^2}{2}-\\frac{r^4}{4}]_0^1=\\frac{\\pi}{2}', font_size=22)
        candidate_objects[(8, 0)] = MathTex('\\frac{\\pi}{2}', font_size=22)
        candidate_objects[(0, 0)] = Text('计算 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(0, 2)] = Text('，其中 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(0, 4)] = Text('，并说明其体积意义。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 0)] = Text('展示 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 2)] = Text('、底面 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 4)] = Text(' 和曲顶 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 6)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 0)] = Text('标出中心高度 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 2)] = Text('、边界高度 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 4)] = Text('；曲面只取圆盘上非负部分。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 0)] = Text('用每个单元的采样点高度画有限立柱，标其体积 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 2)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 0)] = Text('显示黎曼和随分割加细趋于二重积分，', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 0)] = Text('不把有限立柱画面称为精确曲顶实体。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 0)] = Text('切换极坐标，明确面积元 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 2)] = Text(' 和积分范围。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(7, 0)] = Text('展示完整计算 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(7, 2)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_rows = []
        candidate_rows.append(VGroup(candidate_objects[(0, 0)], candidate_objects[(0, 1)], candidate_objects[(0, 2)], candidate_objects[(0, 3)], candidate_objects[(0, 4)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(1, 0)], candidate_objects[(1, 1)], candidate_objects[(1, 2)], candidate_objects[(1, 3)], candidate_objects[(1, 4)], candidate_objects[(1, 5)], candidate_objects[(1, 6)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(2, 0)], candidate_objects[(2, 1)], candidate_objects[(2, 2)], candidate_objects[(2, 3)], candidate_objects[(2, 4)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(3, 0)], candidate_objects[(3, 1)], candidate_objects[(3, 2)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(4, 0)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(5, 0)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(6, 0)], candidate_objects[(6, 1)], candidate_objects[(6, 2)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(7, 0)], candidate_objects[(7, 1)], candidate_objects[(7, 2)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(8, 0)]).arrange(RIGHT, buff=0.12))
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
