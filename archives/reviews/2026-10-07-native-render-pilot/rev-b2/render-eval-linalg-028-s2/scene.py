from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\mathbb R^2',
            '\\alpha=(2,3)',
            '\\beta_1=(1,2)',
            '\\beta_2=(1,1)',
            '\\{\\beta_1,\\beta_2\\}',
            'P=\\begin{pmatrix}1&1\\\\2&1\\end{pmatrix}',
            '\\alpha=P\\xi',
            '\\xi',
            'P^{-1}=\\dfrac{1}{1-2}\\begin{pmatrix}1&-1\\\\-2&1\\end{pmatrix}=\\begin{pmatrix}-1&1\\\\2&-1\\end{pmatrix}',
            '\\xi=P^{-1}\\alpha=\\begin{pmatrix}-1&1\\\\2&-1\\end{pmatrix}\\begin{pmatrix}2\\\\3\\end{pmatrix}=\\begin{pmatrix}-2+3\\\\4-3\\end{pmatrix}=\\begin{pmatrix}1\\\\1\\end{pmatrix}',
            '(1,1)',
            'P^{-1}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
