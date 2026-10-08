from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('y=2x-1', color=YELLOW)
        title = MathTex('f(x)=x^2 \\quad x=1').scale_to_fit_width(config.frame_width - 1.2)
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
        s0 = Text('第一步：动态绘制带有刻度的横纵坐标轴。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：从左侧向右侧，动态绘制出蓝色抛物线 $y=x^2', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：在坐标 $(1,1)$ 的位置闪烁并显示一个黄色', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
        self.play(FadeIn(s2))
        self.wait(0.15)
        s3 = Text('第四步：从黄色圆点处向外延伸出一条橙色直线，表示切线 $', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 3))
        self.play(FadeIn(s3))
        self.wait(0.15)
        s4 = Text("第五步：在画面右下角，用白色字体依次显示导数公式 $f'", font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 4))
        self.play(FadeIn(s4))
        self.wait(0.15)
        ans = answer_math.scale_to_fit_width(config.frame_width - 2)
        ans.to_edge(DOWN)
        self.play(FadeIn(ans))
        self.wait(0.6)



if __name__ == '__main__':
    pass
