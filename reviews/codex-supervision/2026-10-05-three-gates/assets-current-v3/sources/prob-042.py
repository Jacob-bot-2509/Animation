from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('0.5', color=YELLOW)
        title = Text('(公式段提取失败)', font='Microsoft YaHei', font_size=24).to_edge(UP)
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
        s0 = Text('第一步：在坐标系中画出横轴（试验次数 n）和纵轴（正面频', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：模拟抛硬币过程，随着硬币不断被抛出（动态画面），', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：折线在初始阶段（n 较小时）波动剧烈，经常上下大', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
        self.play(FadeIn(s2))
        self.wait(0.15)
        s3 = Text('第四步：随着试验次数 $n$ 增大（如 $n=1000,', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 3))
        self.play(FadeIn(s3))
        self.wait(0.15)
        s4 = Text('第五步：最终，折线几乎紧贴并收敛于红色虚线 $y=0.5', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 4))
        self.play(FadeIn(s4))
        self.wait(0.15)
        ans = answer_math.scale_to_fit_width(config.frame_width - 2)
        ans.to_edge(DOWN)
        self.play(FadeIn(ans))
        self.wait(0.6)



if __name__ == '__main__':
    pass
