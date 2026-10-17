        from math import isfinite as candidate_isfinite
        if self.mobjects:
            raise ValueError('candidate_requires_dedicated_empty_canvas')
        candidate_width = config.frame_width - 1
        candidate_height = config.frame_height - 1
        if not candidate_isfinite(candidate_width) or not candidate_isfinite(candidate_height) or candidate_width <= 0 or candidate_height <= 0:
            raise ValueError('candidate_invalid_viewport')
        candidate_objects = {}
        candidate_objects[(0, 1)] = MathTex('a>0', font_size=22)
        candidate_objects[(0, 3)] = MathTex('L:x^2+y^2=a^2', font_size=22)
        candidate_objects[(0, 5)] = MathTex('\\oint_L x\\,dy-y\\,dx', font_size=22)
        candidate_objects[(1, 1)] = MathTex('x^2+y^2=a^2', font_size=22)
        candidate_objects[(1, 3)] = MathTex('a>0', font_size=22)
        candidate_objects[(2, 1)] = MathTex('t', font_size=22)
        candidate_objects[(3, 1)] = MathTex('D', font_size=22)
        candidate_objects[(3, 3)] = MathTex('\\pi a^2', font_size=22)
        candidate_objects[(4, 1)] = MathTex('(x,y)', font_size=22)
        candidate_objects[(4, 3)] = MathTex('(-y,x)', font_size=22)
        candidate_objects[(6, 1)] = MathTex('P=-y', font_size=22)
        candidate_objects[(6, 3)] = MathTex('Q=x', font_size=22)
        candidate_objects[(6, 5)] = MathTex('Q_x-P_y=2', font_size=22)
        candidate_objects[(7, 1)] = MathTex('2\\pi a^2', font_size=22)
        candidate_objects[(7, 3)] = MathTex('a^2\\int_0^{2\\pi}dt', font_size=22)
        candidate_objects[(8, 0)] = MathTex('2\\pi a^2', font_size=22)
        candidate_objects[(0, 0)] = Text('设 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(0, 2)] = Text('，利用格林公式计算正向圆周 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(0, 4)] = Text(' 上的积分 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(0, 6)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 0)] = Text('绘制圆周 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 2)] = Text('，标明 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(1, 4)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 0)] = Text('以 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(2, 2)] = Text(' 增大对应的逆时针方向标注正向边界。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 0)] = Text('填充内部圆盘 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 2)] = Text('，标面积 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(3, 4)] = Text('。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 0)] = Text('在每个选定点 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 2)] = Text(' 画方向与 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(4, 4)] = Text(' 一致的向量；', font='Microsoft YaHei', font_size=22)
        candidate_objects[(5, 0)] = Text('箭长若作统一缩放须说明，不能任意随机方向。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 0)] = Text('展示 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 2)] = Text('、', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 4)] = Text(' 与 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(6, 6)] = Text('，再用格林公式。', font='Microsoft YaHei', font_size=22)
        candidate_objects[(7, 0)] = Text('给出面积积分 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(7, 2)] = Text('，并用参数式 ', font='Microsoft YaHei', font_size=22)
        candidate_objects[(7, 4)] = Text(' 独立核对。', font='Microsoft YaHei', font_size=22)
        candidate_rows = []
        candidate_rows.append(VGroup(candidate_objects[(0, 0)], candidate_objects[(0, 1)], candidate_objects[(0, 2)], candidate_objects[(0, 3)], candidate_objects[(0, 4)], candidate_objects[(0, 5)], candidate_objects[(0, 6)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(1, 0)], candidate_objects[(1, 1)], candidate_objects[(1, 2)], candidate_objects[(1, 3)], candidate_objects[(1, 4)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(2, 0)], candidate_objects[(2, 1)], candidate_objects[(2, 2)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(3, 0)], candidate_objects[(3, 1)], candidate_objects[(3, 2)], candidate_objects[(3, 3)], candidate_objects[(3, 4)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(4, 0)], candidate_objects[(4, 1)], candidate_objects[(4, 2)], candidate_objects[(4, 3)], candidate_objects[(4, 4)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(5, 0)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(6, 0)], candidate_objects[(6, 1)], candidate_objects[(6, 2)], candidate_objects[(6, 3)], candidate_objects[(6, 4)], candidate_objects[(6, 5)], candidate_objects[(6, 6)]).arrange(RIGHT, buff=0.12))
        candidate_rows.append(VGroup(candidate_objects[(7, 0)], candidate_objects[(7, 1)], candidate_objects[(7, 2)], candidate_objects[(7, 3)], candidate_objects[(7, 4)]).arrange(RIGHT, buff=0.12))
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
