from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('2\\sum_{n=1}^{\\infty} \\frac{(-1)^{n+1}}{n} \\sin(nx)', color=YELLOW)
        title = MathTex('f(x) = x \\quad -\\pi \\le x \\le \\pi').scale_to_fit_width(config.frame_width - 1.2)
        title.to_edge(UP)
        self.play(Write(title))
        circle = Circle(radius=2, color=BLUE)
        self.play(Create(circle))
        radius = Line(ORIGIN, 2 * RIGHT, color=WHITE)
        arc = Arc(radius=2, angle=PI / 4, color=YELLOW)
        self.play(Create(radius), Create(arc))
        tri = Polygon(ORIGIN, 2 * RIGHT,
                       2 * np.array([np.cos(PI / 4), np.sin(PI / 4), 0]),
                       color=GREEN, fill_opacity=0.15)
        self.play(FadeIn(tri))
        lbl = MathTex(r'\frac{\sin(x/2)}{x/2}\to 1').shift(DOWN * 1.6)
        self.play(Write(lbl))
        self.wait(0.4)
        s0 = Text('第一步：画出目标直线 $y=x$（灰色虚线，便于对比）。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：为了视觉效率，不一次性展示所有正弦波，而是先画出', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：采用颜色区分（红、绿、蓝）依次快速叠加第二项和第', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
        self.play(FadeIn(s2))
        self.wait(0.15)
        s3 = Text('第四步：直接展示前10项叠加后的合成波形（黄色粗线），高', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 3))
        self.play(FadeIn(s3))
        self.wait(0.15)
        s4 = Text('第五步：最后展示吉布斯现象在 $x=\\pi$ 处的尖峰，', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 4))
        self.play(FadeIn(s4))
        self.wait(0.15)
        ans = answer_math.scale_to_fit_width(config.frame_width - 2)
        ans.to_edge(DOWN)
        self.play(FadeIn(ans))
        self.wait(0.6)



if __name__ == '__main__':
    pass
