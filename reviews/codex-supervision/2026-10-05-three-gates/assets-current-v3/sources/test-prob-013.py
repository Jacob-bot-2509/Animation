from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('M(t)=e^{\\lambda(e^t-1)} \\quad E[X]=\\lambda \\quad E[X^2]=\\lambda^2+\\lambda', color=YELLOW)
        title = MathTex('X\\sim\\operatorname{Poisson}(\\lambda) \\quad M(t) \\quad E[X] \\quad E[X^2]').scale_to_fit_width(config.frame_width - 1.2)
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
        s0 = Text('第一步：建立概率论·矩母函数×数字特征综合场景，呈现与矩', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：矩母函数曲线。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：导数与矩的对应。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
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
