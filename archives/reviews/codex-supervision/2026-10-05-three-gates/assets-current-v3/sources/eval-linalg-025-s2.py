from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('x-1 \\quad 3 \\quad x^2+1 \\quad 2x+1', color=YELLOW)
        title = MathTex('f(x)=x^5+x+1 \\quad f(x) \\quad x-1 \\quad x^2+1').scale_to_fit_width(config.frame_width - 1.2)
        title.to_edge(UP)
        self.play(Write(title))
        s0 = Text('第一步：以长除法为主线，建立高等代数·多项式场景并呈现该', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：长除法竖式动画。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：商 $x^3-x$ 与余式 $2x+1$ 的提取', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
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
