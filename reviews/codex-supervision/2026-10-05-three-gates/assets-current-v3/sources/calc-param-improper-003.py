from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('\\frac{1}{\\alpha}', color=YELLOW)
        title = MathTex('I(\\alpha) = \\int_{0}^{+\\infty} e^{-\\alpha x}dx \\quad \\alpha>0').scale_to_fit_width(config.frame_width - 1.2)
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
        s0 = Text('第一步：绘制坐标系，先展示$\\alpha =1$时的标准', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：在屏幕上方显示一个“参数滑块”，动态演示改变$\\', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：随着参数滑块的移动，曲线随之变陡或变平，展示$\\', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
        self.play(FadeIn(s2))
        self.wait(0.15)
        s3 = Text('第四步：在曲线下方持续保持黄色面积填充，直观展示面积随参', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 3))
        self.play(FadeIn(s3))
        self.wait(0.15)
        s4 = Text('第五步：画面清晰显示推导过程$\\lim_{b\\to +\\', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 4))
        self.play(FadeIn(s4))
        self.wait(0.15)
        ans = answer_math.scale_to_fit_width(config.frame_width - 2)
        ans.to_edge(DOWN)
        self.play(FadeIn(ans))
        self.wait(0.6)



if __name__ == '__main__':
    pass
