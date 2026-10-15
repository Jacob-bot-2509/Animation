from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('1,\\ 1,\\ (\\lambda-a)(\\lambda-1)^2 \\quad a\\neq 1 \\quad \\lambda-a \\quad (\\lambda-1)^2 \\quad a=1 \\quad (\\lambda-1)^3', color=YELLOW)
        title = MathTex('a\\in\\mathbb R \\quad \\lambda \\quad A(\\lambda)=\\begin{pmatrix}\\lambda-a&1&0\\\\0&\\lambda-1&1\\\\0&0&\\lambda-1\\end{pmatrix} \\quad A(\\lambda) \\quad a').scale_to_fit_width(config.frame_width - 1.2)
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
        s0 = Text('第一步：以行列式因子为主线，建立高等代数·λ-矩阵场景并', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：全部二阶子式 $\\gcd=1$ 的逐一检验。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：$a$ 滑杆下 $(\\lambda-a)$ 与 ', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
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
