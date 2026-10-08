from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('\\pi \\approx \\frac{4m}{n}', color=YELLOW)
        title = MathTex('\\pi').scale_to_fit_width(config.frame_width - 1.2)
        title.to_edge(UP)
        self.play(Write(title))
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 4, 1],
                  x_length=7, y_length=4).shift(DOWN * 0.6)
        self.play(Create(ax))
        bars = VGroup(*[
            Rectangle(width=0.7, height=h, color=TEAL, fill_opacity=0.6)
            .move_to(ax.c2p(x, 0), aligned_edge=DOWN).shift(UP * h / 2)
            for x, h in zip([1, 2, 3, 4, 5], [1, 3, 2, 3, 1])])
        self.play(FadeIn(bars))
        curve = ax.plot(lambda x: 2.2 * np.exp(-((x - 2.5) ** 2) / 1.2),
                        x_range=[0, 5.5, 0.01], color=YELLOW)
        self.play(Create(curve))
        self.wait(0.4)
        s0 = Text('第一步：绘制一个边长为2，中心在原点的正方形，并画出它的', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：用程序生成均匀分布的随机点，让这些点像下雨一样落', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：落在圆内的点显示为蓝色，落在圆外的点显示为灰色，', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
        self.play(FadeIn(s2))
        self.wait(0.15)
        s3 = Text('第四步：右侧实时展示估算公式 $\\pi \\approx ', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 3))
        self.play(FadeIn(s3))
        self.wait(0.15)
        s4 = Text('第五步：对比展示理论值，直观揭示频率的稳定性和大数定律。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 4))
        self.play(FadeIn(s4))
        self.wait(0.15)
        ans = answer_math.scale_to_fit_width(config.frame_width - 2)
        ans.to_edge(DOWN)
        self.play(FadeIn(ans))
        self.wait(0.6)



if __name__ == '__main__':
    pass
