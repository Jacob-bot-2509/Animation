from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('\\dfrac{2}{\\pi}', color=YELLOW)
        title = MathTex('\\displaystyle\\lim_{n\\to\\infty}\\frac{1}{n}\\sum_{k=1}^{n}\\sin\\frac{k\\pi}{n}').scale_to_fit_width(config.frame_width - 1.2)
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
        s0 = Text('第一步：建立数学分析·极限×定积分综合场景，呈现与黎曼和', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：单位区间 $[0,1]$ 上 $\\sin(\\pi', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：和式随 $n$ 增大收敛于积分值。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
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
