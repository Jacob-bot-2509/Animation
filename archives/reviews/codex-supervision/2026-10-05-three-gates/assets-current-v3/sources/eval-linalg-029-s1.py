from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('\\ker T=\\{(0,0)\\} \\quad \\operatorname{Im}T=\\mathbb R^2 \\quad \\dim\\ker T+\\dim\\operatorname{Im}T=2', color=YELLOW)
        title = MathTex('T:\\mathbb R^2\\to\\mathbb R^2 \\quad T(x,y)=(x+2y,2x+y) \\quad \\ker T \\quad \\operatorname{Im}T').scale_to_fit_width(config.frame_width - 1.2)
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
        s0 = Text('第一步：以矩阵行列式为主线，建立高等代数·线性变换场景并', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：行列式 $\\det A=-3\\ne0$ 的可逆判', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：核为零、像为全空间的标注。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
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
