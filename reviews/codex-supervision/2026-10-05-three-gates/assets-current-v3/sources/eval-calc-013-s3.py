from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('(x^2-2x+2)e^x+C', color=YELLOW)
        title = MathTex('\\displaystyle\\int x^2e^x\\,dx').scale_to_fit_width(config.frame_width - 1.2)
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
        s0 = Text('第一步：以递推公式为主线，建立数学分析·不定积分场景并呈', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：递推链 $I_0\\to I_1\\to I_2$ ', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：递推式 $I_n=x^ne^x-nI_{n-1}', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
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
