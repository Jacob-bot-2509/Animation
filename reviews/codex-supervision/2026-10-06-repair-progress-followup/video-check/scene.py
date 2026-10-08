
from manim import *

class ConceptScene(Scene):
    def construct(self):
        title = Text('求矩阵对应的线性变换对二维平面的几何影响',
                     font='Microsoft YaHei', font_size=24, color=WHITE).to_edge(UP)
        formula = MathTex(r'T(x,y)=(x+3y,\,y),\qquad \det A=1',
                          color=WHITE).scale(3/4).next_to(title, DOWN)
        panel = Rectangle(width=8.8, height=3.9, fill_color=GRAY_A,
                          fill_opacity=1, stroke_width=0).shift(DOWN*0.4)
        axes = Axes(x_range=[-0.5, 5.5, 1], y_range=[-0.5, 2.2, 1],
                    x_length=7.4, y_length=2.6,
                    axis_config={'color': BLACK, 'include_numbers': True,
                                 'font_size': 15,
                                 'decimal_number_config': {'color': BLACK,
                                                           'num_decimal_places': 0}})
        axes.move_to(panel.get_center() + DOWN*0.05)

        sq_pts = [(0,0), (1,0), (1,1), (0,1)]
        pa_pts = [(0,0), (1,0), (4,1), (3,1)]
        square = Polygon(*[axes.c2p(*p) for p in sq_pts],
                         color=BLUE, fill_opacity=0.2)
        sq_verts = VGroup(*[Dot(axes.c2p(*p), color=BLUE, radius=0.06)
                            for p in sq_pts])
        para = Polygon(*[axes.c2p(*p) for p in pa_pts],
                       color=ORANGE, fill_opacity=0.2)
        pa_verts = VGroup(*[Dot(axes.c2p(*p), color=ORANGE, radius=0.06)
                            for p in pa_pts])
        pa_labels = VGroup(*[
            MathTex(r'(%d,%d)' % p, color=WHITE).scale(1/2).next_to(
                axes.c2p(*p), UL if p[1] == 0 else UR)
            for p in pa_pts])

        def seg(y):
            dots = VGroup(Dot(axes.c2p(0, y), color=TEAL, radius=0.06),
                          Dot(axes.c2p(1, y), color=TEAL, radius=0.06))
            return VGroup(Line(axes.c2p(0, y), axes.c2p(1, y), color=TEAL), dots)
        seg1, seg1_img = seg(1/2), seg(1/2)
        seg1_img.shift(axes.c2p(3/2, 0) - axes.c2p(0, 0))
        seg2, seg2_img = seg(1), seg(1)
        seg2_img.shift(axes.c2p(3, 0) - axes.c2p(0, 0))
        caption3 = Text('水平直线作为集合不变，线上点位移 (3y, 0)',
                        font='Microsoft YaHei', font_size=20,
                        color=WHITE).to_edge(DOWN)
        caption4 = Text('单位正方形变为底 1 高 1 的平行四边形，面积不变',
                        font='Microsoft YaHei', font_size=20,
                        color=WHITE).to_edge(DOWN)
        vline = Line(axes.c2p(1/2, -0.3), axes.c2p(1/2, 1.2), color=GREEN)
        vline_img = Line(axes.c2p(1/2 - 0.9, -0.3), axes.c2p(1/2 + 3.6, 1.2),
                         color=GREEN)
        vlabel = MathTex(r'X-3Y=c', color=WHITE).scale(1/2).next_to(
            axes.c2p(4.1, 1.2), UR)
        e2_dot = Dot(axes.c2p(0, 1), color=YELLOW, radius=0.07)
        e2_img = Dot(axes.c2p(3, 1), color=YELLOW, radius=0.07)
        e2_label = MathTex(r'\sqrt{10}', color=WHITE).scale(1/2).next_to(
            axes.c2p(3, 1), UR)

        self.add(title, panel)
        self.play(Create(axes))
        self.play(Create(square), Create(sq_verts))
        self.play(Write(formula))
        self.play(Transform(seg1, seg1_img), Transform(seg2, seg2_img),
                  run_time=1.5)
        self.play(Write(caption3))
        self.wait(1/2)
        self.play(Transform(square, para), Transform(sq_verts, pa_verts),
                  run_time=1.5)
        self.play(Write(caption4), Write(pa_labels))
        self.wait(1/2)
        self.play(Create(vline), Create(e2_dot))
        self.play(Transform(vline, vline_img), Write(vlabel),
                  Transform(e2_dot, e2_img), Write(e2_label), run_time=1.5)
        self.wait(1)
