from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('x \\quad y \\quad y+3x', color=YELLOW)
        title = MathTex('E=\\begin{pmatrix} 1 & 0 \\\\ 3 & 1 \\end{pmatrix}').scale_to_fit_width(config.frame_width - 1.2)
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
        s0 = Text('第一步：画出标准网格和单位正方形。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：应用初等矩阵 E 的变换，展示水平网格线发生倾斜', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：观察单位正方形变为平行四边形（以仍竖直的边为底，', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
        self.play(FadeIn(s2))
        self.wait(0.15)
        s3 = Text('第四步：高亮显示行列式值为 1，说明剪切变换不改变面积。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 3))
        self.play(FadeIn(s3))
        self.wait(0.15)
        ans = answer_math.scale_to_fit_width(config.frame_width - 2)
        ans.to_edge(DOWN)
        self.play(FadeIn(ans))
        self.wait(0.6)



if __name__ == '__main__':
    pass
