from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex("\\dfrac{f''(0)}{2}", color=YELLOW)
        title = MathTex("f \\quad f(0)=f'(0)=0 \\quad \\displaystyle\\lim_{x\\to 0}\\frac{f(x)}{x^2}").scale_to_fit_width(config.frame_width - 1.2)
        title.to_edge(UP)
        self.play(Write(title))
        ax = Axes(x_range=[-3, 3, 1], y_range=[-1, 3, 1],
                  x_length=7, y_length=4).shift(DOWN * 0.6)
        self.play(Create(ax))
        curve = ax.plot(lambda x: np.sin(x) / x if abs(x) > 1e-6 else 1.0,
                        x_range=[-3, 3, 0.01], color=BLUE)
        self.play(Create(curve))
        lim = ax.get_vertical_line(ax.c2p(0, 1), color=YELLOW)
        dot = Dot(ax.c2p(0, 1), color=RED)
        self.play(Create(lim), FadeIn(dot))
        lbl = MathTex(r'x\to 0').next_to(lim, RIGHT)
        self.play(Write(lbl))
        self.wait(0.4)
        s0 = Text('第一步：建立数学分析·中值定理×极限综合场景，呈现与洛必', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：洛必达两步的分子分母比值。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：$f$ 在原点附近的二阶接触。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
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
