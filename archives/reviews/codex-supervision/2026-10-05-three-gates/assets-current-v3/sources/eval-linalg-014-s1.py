from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('1,\\ 1+\\sqrt{2}a,\\ 1-\\sqrt{2}a \\quad \\dfrac{1}{\\sqrt{2}}(1,0,-1)^T,\\ \\dfrac{1}{2}(1,\\sqrt{2},1)^T,\\ \\dfrac{1}{2}(1,-\\sqrt{2},1)^T \\quad Q=\\begin{pmatrix}1/\\sqrt{2}&1/2&1/2\\\\0&\\sqrt{2}/2&-\\sqrt{2}/2\\\\-1/\\sqrt{2}&1/2&1/2\\end{pmatrix} \\quad Q^TAQ=\\operatorname{diag}(1,\\,1+\\sqrt{2}a,\\,1-\\sqrt{2}a)', color=YELLOW)
        title = MathTex('a\\in\\mathbb R\\setminus\\{0\\} \\quad A=\\begin{pmatrix}1&a&0\\\\a&1&a\\\\0&a&1\\end{pmatrix} \\quad Q \\quad Q^TAQ').scale_to_fit_width(config.frame_width - 1.2)
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
        s0 = Text('第一步：以特征方程为主线，建立高等代数·特征值与特征向量', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：三阶特征多项式按第一列展开与因式分解。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：三个特征方向上伸缩率 $1,\\ 1\\pm\\sqr', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
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
