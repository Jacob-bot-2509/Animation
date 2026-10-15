from manim import *
import numpy as np


class PilotScene(Scene):
    def construct(self):
        answer_math = MathTex('3x+2y=6\\sqrt{2}', color=YELLOW)
        title = MathTex('\\dfrac{x^2}{4}+\\dfrac{y^2}{9}=1 \\quad \\left(\\sqrt{2},\\dfrac{3}{\\sqrt{2}}\\right)').scale_to_fit_width(config.frame_width - 1.2)
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
        s0 = Text('第一步：以参数化求导为主线，建立解析几何·二次曲线场景并', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 0))
        self.play(FadeIn(s0))
        self.wait(0.15)
        s1 = Text('第二步：参数化 $x=2\\cos t$、$y=3\\sin', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 1))
        self.play(FadeIn(s1))
        self.wait(0.15)
        s2 = Text('第三步：切点沿椭圆滑动的切线族。', font='Microsoft YaHei', font_size=22).shift(DOWN * (1.2 + 0.6 * 2))
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
