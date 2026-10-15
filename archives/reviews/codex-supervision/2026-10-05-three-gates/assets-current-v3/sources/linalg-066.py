from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('\\begin{pmatrix} 2 & 1 & 0 \\\\ 0 & 2 & 0 \\\\ 0 & 0 & 3 \\end{pmatrix}', color=YELLOW)
        title = MathTex('A=\\begin{pmatrix} 2 & 1 & 0 \\\\ 0 & 2 & 0 \\\\ 0 & 0 & 3 \\end{pmatrix}').scale_to_fit_width(config.frame_width - 1.2)
        title.to_edge(UP)
        self.play(Write(title))
        m = Matrix([[1, 2], [0, 1]], h_buff=0.9)
        self.play(Write(m))
        brace = Brace(m, DOWN)
        lbl = MathTex(r'B^2=A').next_to(brace, DOWN)
        self.play(GrowFromCenter(brace), FadeIn(lbl))
        arrow = Arrow(LEFT * 3, LEFT * 1.5, color=YELLOW)
        self.play(Create(arrow))
        self.wait(0.4)
        s0 = Text('第一步：展示矩阵 A，用不同颜色标出两个若尔当块。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：用动画高亮矩阵的分块结构，直观展示两个若尔当块。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：高亮 2×2 的若尔当块，展示其主对角线为 2、', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
        self.play(FadeIn(s2))
        self.wait(0.15)
        s3 = Text('第四步：标注 1×1 的若尔当块对应特征值 3，可以单独', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 3))
        self.play(FadeIn(s3))
        self.wait(0.15)
        ans = answer_math.scale_to_fit_width(config.frame_width - 2)
        ans.to_edge(DOWN)
        self.play(FadeIn(ans))
        self.wait(0.6)



if __name__ == '__main__':
    pass
