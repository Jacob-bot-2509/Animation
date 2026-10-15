from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('\\ln 2', color=YELLOW)
        title = MathTex('\\displaystyle\\sum_{n=1}^{\\infty}\\frac{1}{n\\cdot 2^n}').scale_to_fit_width(config.frame_width - 1.2)
        title.to_edge(UP)
        self.play(Write(title))
        line = NumberLine(x_range=[0, 12, 1], length=9).shift(DOWN * 1.2)
        self.play(Create(line))
        dots = VGroup(*[Dot(line.n2p(n), color=TEAL)
                        for n in range(1, 9)])
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.15))
        lbl = MathTex(r'a_n', color=YELLOW).shift(UP * 1.5)
        self.play(Write(lbl))
        self.wait(0.4)
        s0 = Text('第一步：以代入对数展开式为主线，建立数学分析·幂级数场景', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：展开式 $-\\ln(1-x)=x+\\dfrac{', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：$x=\\dfrac{1}{2}$ 代入的标注。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
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
