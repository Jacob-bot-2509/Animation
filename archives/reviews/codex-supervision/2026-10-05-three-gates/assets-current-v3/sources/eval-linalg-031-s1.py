from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('\\operatorname{diag}\\!\\bigl(J_2(2),\\,2,\\,3\\bigr)=\\begin{pmatrix}2&1&0&0\\\\0&2&0&0\\\\0&0&2&0\\\\0&0&0&3\\end{pmatrix} \\quad J_2(2)=\\begin{pmatrix}2&1\\\\0&2\\end{pmatrix}', color=YELLOW)
        title = MathTex('A \\quad m_A(\\lambda)=(\\lambda-2)^2(\\lambda-3) \\quad \\operatorname{tr}(A)=9 \\quad A').scale_to_fit_width(config.frame_width - 1.2)
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
        s0 = Text('第一步：以最小多项式定最大块阶为主线，建立高等代数·λ-', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：若尔当块按 $(\\lambda-2)^2$、$(', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：迹 9 排除 $10$ 的组合。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
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
