from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        title = MathTex(r'设 $X$ 服从参数 $p=\\dfrac{1}{2}$ 的几何分布（抛硬币直到正面）。求 $P(X$ 为偶数$)$ 的精确值。').scale_to_fit_width(config.frame_width - 1.2)
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
        s0 = Text('第一步：建立跨学科·概率论×级数综合场景，呈现与几何分布', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：奇偶分支的概率条。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：几何级数求和示意。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
        self.play(FadeIn(s2))
        self.wait(0.15)
        s3 = Text('第四步：高亮最终结果与答案。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 3))
        self.play(FadeIn(s3))
        self.wait(0.15)
        ans = MathTex(r'$\\dfrac{1}{3}$', color=YELLOW).scale_to_fit_width(config.frame_width - 2)
        ans.to_edge(DOWN)
        self.play(FadeIn(ans))
        self.wait(0.6)



if __name__ == '__main__':
    pass
