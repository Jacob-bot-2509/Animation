from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        title = MathTex('A=\\begin{pmatrix} \\cos\\theta & -\\sin\\theta \\\\ \\sin\\theta & \\cos\\theta \\end{pmatrix}').scale_to_fit_width(config.frame_width - 1.2)
        title.to_edge(UP)
        self.play(Write(title))
        circle = Circle(radius=2, color=BLUE)
        self.play(Create(circle))
        radius = Line(ORIGIN, 2 * RIGHT, color=WHITE)
        arc = Arc(radius=2, angle=PI / 4, color=YELLOW)
        self.play(Create(radius), Create(arc))
        tri = Polygon(ORIGIN, 2 * RIGHT,
                       2 * np.array([np.cos(PI / 4), np.sin(PI / 4), 0]),
                       color=GREEN, fill_opacity=0.15)
        self.play(FadeIn(tri))
        lbl = MathTex(r'\frac{\sin(x/2)}{x/2}\to 1').shift(DOWN * 1.6)
        self.play(Write(lbl))
        self.wait(0.4)
        s0 = Text('第一步：在坐标系中画出一个三角形，标注其边长和角度。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：应用正交变换（旋转 θ 角），展示三角形绕原点旋', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：用动态测量工具验证旋转后三角形的边长和角度完全不', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
        self.play(FadeIn(s2))
        self.wait(0.15)
        s3 = Text('第四步：高亮矩阵列向量是标准正交基，展示 AᵀA=I。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 3))
        self.play(FadeIn(s3))
        self.wait(0.15)
        self.wait(0.3)



if __name__ == '__main__':
    pass
