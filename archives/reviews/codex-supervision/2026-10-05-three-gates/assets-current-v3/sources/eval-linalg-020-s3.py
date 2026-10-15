from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        title = MathTex('f(x,y)=x^2-4xy+4y^2').scale_to_fit_width(config.frame_width - 1.2)
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
        s0 = Text('第一步：以几何观点为主线，建立高等代数·二次型场景并呈现', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：平行直线对等值线族。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：退化椭圆的极限示意。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
        self.play(FadeIn(s2))
        self.wait(0.15)
        s3 = Text('第四步：高亮最终结果与答案。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 3))
        self.play(FadeIn(s3))
        self.wait(0.15)
        self.wait(0.3)



if __name__ == '__main__':
    pass
