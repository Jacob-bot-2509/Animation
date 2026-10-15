from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('u_1=(1,1,0) \\quad u_2=(1,-1,2) \\quad u_3=(1,-1,-1)', color=YELLOW)
        title = MathTex('(1,1,0),(1,0,1),(0,1,1)').scale_to_fit_width(config.frame_width - 1.2)
        title.to_edge(UP)
        self.play(Write(title))
        s0 = Text('第一步：以对称性构造为主线，建立高等代数·线性空间场景并', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：和向量/差向量/叉积的轮换对称构造。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：替代正交基的标注。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
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
