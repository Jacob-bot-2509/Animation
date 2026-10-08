from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('(1,1)', color=YELLOW)
        title = MathTex('\\mathbb R^2 \\quad \\alpha=(2,3) \\quad \\beta_1=(1,2) \\quad \\beta_2=(1,1)').scale_to_fit_width(config.frame_width - 1.2)
        title.to_edge(UP)
        self.play(Write(title))
        tri = Polygon(ORIGIN + DOWN * 0.8, 2 * RIGHT + DOWN * 0.8,
                       1.2 * UP + 0.3 * RIGHT,
                       color=BLUE, fill_opacity=0.1)
        self.play(Create(tri))
        circ = Circle(radius=0.7, color=GREEN).move_to(0.8 * RIGHT)
        self.play(Create(circ))
        right = RightAngle(Line(tri.get_vertices()[0], tri.get_vertices()[1]),
                           Line(tri.get_vertices()[1], tri.get_vertices()[2]),
                           length=0.25, color=YELLOW)
        self.play(Create(right))
        self.wait(0.4)
        s0 = Text('第一步：以几何分解为主线，建立高等代数·线性空间场景并呈', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：斜基网格与平行四边形分解。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：$\\beta_1+\\beta_2=(2,3)$ ', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
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
