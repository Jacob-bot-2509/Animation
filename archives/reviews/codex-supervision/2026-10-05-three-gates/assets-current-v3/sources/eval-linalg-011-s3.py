from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('\\lambda\\ne 1 \\quad \\lambda\\ne-2 \\quad \\lambda=1 \\quad \\lambda=-2', color=YELLOW)
        title = MathTex('\\begin{cases}\\lambda x+y+z=1\\\\x+\\lambda y+z=\\lambda\\\\x+y+\\lambda z=\\lambda^2\\end{cases}').scale_to_fit_width(config.frame_width - 1.2)
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
        s0 = Text('第一步：以几何观点为主线，建立高等代数·线性方程组场景并', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：$\\lambda$ 滑块下三平面的位置变化。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：重合/交于一点/无公共点的三种几何。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
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
