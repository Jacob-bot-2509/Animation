from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('f_1(x,y)=x, f_2(x,y)=y', color=YELLOW)
        title = MathTex('V=\\mathbb{R}^2 \\quad \\varepsilon_1=(1,0), \\varepsilon_2=(0,1) \\quad f_1, f_2 \\quad f_i(\\varepsilon_j)=\\delta_{ij}').scale_to_fit_width(config.frame_width - 1.2)
        title.to_edge(UP)
        self.play(Write(title))
        s0 = Text('第一步：在二维空间中画出标准基向量 ε₁ 和 ε₂。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：画出线性函数 f₁(x,y)=x 的等值线（竖直', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：画出 f₂(x,y)=y 的等值线（水平线），展', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
        self.play(FadeIn(s2))
        self.wait(0.15)
        s3 = Text('第四步：高亮对偶基的克罗内克 δ 性质。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 3))
        self.play(FadeIn(s3))
        self.wait(0.15)
        ans = answer_math.scale_to_fit_width(config.frame_width - 2)
        ans.to_edge(DOWN)
        self.play(FadeIn(ans))
        self.wait(0.6)



if __name__ == '__main__':
    pass
