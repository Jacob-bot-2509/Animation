from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        title = MathTex('\\sum_{n=1}^{\\infty} \\frac{x^n}{n^2} \\quad [-1, 1]').scale_to_fit_width(config.frame_width - 1.2)
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
        s0 = Text('第一步：绘制直角坐标系，用浅灰色画出两条上下对称的界直线', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：依次绘制前1项、前3项、前5项、前20项的部分和', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：展示随着项数 $N$ 增大，部分和曲线的“波动”', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
        self.play(FadeIn(s2))
        self.wait(0.15)
        s3 = Text('第四步：高亮展示随着 $N$ 增大，部分和曲线在区间 $', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 3))
        self.play(FadeIn(s3))
        self.wait(0.15)
        s4 = Text('第五步：右侧展示 M-判别法的数学推导过程，强调 $\\f', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 4))
        self.play(FadeIn(s4))
        self.wait(0.15)
        self.wait(0.3)



if __name__ == '__main__':
    pass
