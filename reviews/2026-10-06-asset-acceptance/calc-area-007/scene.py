"""Record-specific area candidate. Exact formula; no zero-height rescaling."""
from fractions import Fraction
from manim import *


def area_slice_vertices(x, dx=Fraction(1, 12)):
    if not -1 <= x <= 2 or dx <= 0:
        raise ValueError('Slice outside the integration interval')
    left = max(Fraction(-1), x - dx / 2)
    right = min(Fraction(2), x + dx / 2)
    lower, upper = x ** 2, x + 2
    return [(left, lower), (right, lower), (right, upper), (left, upper)]


class ConceptScene(Scene):
    def construct(self):
        title = MathTex('y=x^2', r'\quad', 'y=x+2').to_edge(UP)
        self.play(Write(title))
        axes = Axes(x_range=[-2, 4, 1], y_range=[-2, 6, 1],
                    x_length=33/5, y_length=19/5).shift(RIGHT + DOWN*9/20)
        curve = axes.plot(lambda x: x**2, x_range=[-3/2, 27/10, 1/100], color=BLUE)
        line = axes.plot(lambda x: x+2, x_range=[-3/2, 27/10, 1/100], color=RED)
        captions = VGroup(*[
            Text(text, font='Microsoft YaHei', font_size=24).scale(9/20)
            for text in ('第一步：画出两条边界曲线', '第二步：标出两个交点',
                         '第三步：填充封闭区域', '第四步：展示面积微元',
                         '第五步：计算定积分面积')
        ]).arrange(DOWN, aligned_edge=LEFT, buff=1/3).to_edge(LEFT, buff=1/3)
        self.play(Create(axes), Create(curve), Create(line), FadeIn(captions[0]))
        points = VGroup(Dot(axes.c2p(-1, 1), color=YELLOW),
                        Dot(axes.c2p(2, 4), color=YELLOW))
        labels = VGroup(MathTex('(-1,1)').scale(11/20).next_to(points[0], DL, buff=3/25),
                        MathTex('(2,4)').scale(11/20).next_to(points[1], UR, buff=3/25))
        self.play(FadeIn(points), Write(labels), FadeIn(captions[1]))
        area = axes.get_area(curve, x_range=[-1, 2], bounded_graph=line,
                             color=YELLOW, opacity=9/20)
        self.play(FadeIn(area), FadeIn(captions[2]))
        value = ValueTracker(-1)
        # Fresh vertices each frame: endpoints may degenerate without division by zero.
        def slice_polygon():
            vertices = area_slice_vertices(value.get_value())
            return Polygon(*[axes.c2p(float(x), float(y)) for x, y in vertices],
                           color=ORANGE, fill_opacity=11/20, stroke_width=0)
        micro_element = always_redraw(slice_polygon)
        self.add(micro_element)
        self.play(FadeIn(captions[3]))
        self.play(value.animate.set_value(2), run_time=9/2)
        self.remove(micro_element)
        formula = MathTex(r'S=\int_{-1}^{2}(x+2-x^2)\,dx',
                          r'=\left[\frac{x^2}{2}+2x-\frac{x^3}{3}\right]_{-1}^{2}',
                          r'=\frac{9}{2}').scale_to_fit_width(config.frame_width-6/5).to_edge(DOWN)
        self.play(Write(formula), FadeIn(captions[4]))
        self.wait(4/5)