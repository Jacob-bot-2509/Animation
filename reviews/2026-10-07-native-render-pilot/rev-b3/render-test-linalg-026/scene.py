from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'f=3x^2+4xy+6y^2',
            'f=3\\left(x^2+\\dfrac{4}{3}xy\\right)+6y^2=3\\left(x+\\dfrac{2}{3}y\\right)^2-\\dfrac{4}{3}y^2+6y^2=3\\left(x+\\dfrac{2}{3}y\\right)^2+\\dfrac{14}{3}y^2',
            'u=x+\\dfrac{2}{3}y',
            'v=y',
            'x=u-\\dfrac{2}{3}v',
            'y=v',
            '3u^2+\\dfrac{14}{3}v^2',
            'A=\\begin{pmatrix}3&2\\\\2&6\\end{pmatrix}',
            'C=\\begin{pmatrix}1&-\\frac{2}{3}\\\\0&1\\end{pmatrix}',
            'C^TAC=\\begin{pmatrix}3&0\\\\0&\\frac{14}{3}\\end{pmatrix}',
            'AC=\\begin{pmatrix}3&0\\\\2&\\frac{14}{3}\\end{pmatrix}',
            'C^T(AC)=\\begin{pmatrix}3&0\\\\0&\\frac{14}{3}\\end{pmatrix}',
            '\\begin{cases}u=x+\\frac{2}{3}y\\\\v=y\\end{cases}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
