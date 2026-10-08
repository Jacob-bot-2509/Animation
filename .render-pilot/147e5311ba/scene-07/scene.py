from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        title = MathTex(r'三门问题：参赛者在三扇门中选择一扇（其中一扇后有汽车，另两扇后是山羊）。主持人（知道车在哪）打开另一扇有山羊的门，给参赛者一次换门机会。问换门获胜的概率是多少？并解释原因。').scale_to_fit_width(config.frame_width - 1.2)
        title.to_edge(UP)
        self.play(Write(title))
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 4, 1],
                  x_length=7, y_length=4).shift(DOWN * 0.6)
        self.play(Create(ax))
        bars = ax.get_bar_chart([1, 3, 2, 3, 1], bar_width=0.7, color=TEAL)
        self.play(FadeIn(bars))
        curve = ax.plot(lambda x: 2.2 * np.exp(-((x - 2.5) ** 2) / 1.2),
                        x_range=[0, 5.5, 0.01], color=YELLOW)
        self.play(Create(curve))
        self.wait(0.4)
        s0 = Text('第一步：以贝叶斯公式为主线，建立概率论·条件概率场景并呈', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：贝叶斯分母三项的条带分解。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：条件概率 $P(C_3|H_2)$ 的收缩动画。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
        self.play(FadeIn(s2))
        self.wait(0.15)
        s3 = Text('第四步：高亮最终结果与答案。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 3))
        self.play(FadeIn(s3))
        self.wait(0.15)
        ans = MathTex(r'换门获胜概率为 $\\dfrac{2}{3}$，不换为 $\\dfrac{1}{3}$', color=YELLOW).scale_to_fit_width(config.frame_width - 2)
        ans.to_edge(DOWN)
        self.play(FadeIn(ans))
        self.wait(0.6)



if __name__ == '__main__':
    pass
