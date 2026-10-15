from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('\\dfrac{3\\pi}{2}', color=YELLOW)
        title = MathTex('\\displaystyle I=\\iint_D(x^2+y^2)\\,dA \\quad D=\\{(x,y):x^2+y^2\\le 2y\\}').scale_to_fit_width(config.frame_width - 1.2)
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
        s0 = Text('第一步：以极坐标为主线，建立数学分析·重积分场景并呈现该', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：圆盘 $D$ 与极角 $\\theta\\in[0,', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：$r^4$ 径向积分与 $\\sin^4\\thet', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
        self.play(FadeIn(s2))
        self.wait(0.15)
        s3 = Text('第四步：高亮最终结果与答案。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 3))
        self.play(FadeIn(s3))
        self.wait(0.15)
        ans = answer_math.scale_to_fit_width(config.frame_width - 2)
        ans.to_edge(DOWN)
        self.play(FadeIn(ans))
        self.wait(0.6)



if __name__ == '__main__':
    pass
