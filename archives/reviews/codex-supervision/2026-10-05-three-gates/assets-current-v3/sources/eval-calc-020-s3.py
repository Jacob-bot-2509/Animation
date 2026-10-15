from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('p>1 \\quad \\dfrac{1}{p-1} \\quad 0<p\\le 1', color=YELLOW)
        title = MathTex('\\displaystyle\\int_1^{+\\infty}\\frac{dx}{x^p} \\quad p>0').scale_to_fit_width(config.frame_width - 1.2)
        title.to_edge(UP)
        self.play(Write(title))
        ax = Axes(x_range=[-2, 4, 1], y_range=[-2, 6, 1],
                  x_length=7, y_length=4).shift(DOWN * 0.6)
        self.play(Create(ax))
        curve = ax.plot(lambda x: x ** 2, x_range=[-2, 3, 0.01], color=BLUE)
        self.play(Create(curve))
        p = ax.c2p(1, 1)
        tangent = ax.plot(lambda x: 2 * x - 1, x_range=[-1, 2.2, 0.01],
                          color=YELLOW)
        dot = Dot(p, color=RED)
        self.play(Create(tangent), FadeIn(dot))
        lbl = MathTex(r"f'(x)=2x").next_to(p, UR)
        self.play(Write(lbl))
        self.wait(0.4)
        s0 = Text('第一步：以面积直觉与分块比较为主线，建立数学分析·反常积', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：$p$ 滑块联动曲线 $y=1/x^p$。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：整数分块条带面积与级数项对照。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
        self.play(FadeIn(s2))
        self.wait(0.15)
        s3 = Text('第四步：临界 $p=1$ 高亮。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 3))
        self.play(FadeIn(s3))
        self.wait(0.15)
        s4 = Text('第五步：高亮最终结果与答案。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 4))
        self.play(FadeIn(s4))
        self.wait(0.15)
        ans = answer_math.scale_to_fit_width(config.frame_width - 2)
        ans.to_edge(DOWN)
        self.play(FadeIn(ans))
        self.wait(0.6)



if __name__ == '__main__':
    pass
