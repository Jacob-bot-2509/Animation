from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\mathbb R^2',
            '\\operatorname{span}\\{(1,1)^T\\}',
            '(3,1)^T',
            '\\hat u=\\dfrac{1}{\\sqrt2}(1,1)^T',
            'P=\\hat u\\hat u^T=\\dfrac{1}{2}\\begin{pmatrix}1&1\\\\1&1\\end{pmatrix}=\\begin{pmatrix}\\frac{1}{2}&\\frac{1}{2}\\\\\\frac{1}{2}&\\frac{1}{2}\\end{pmatrix}',
            'P\\begin{pmatrix}3\\\\1\\end{pmatrix}=\\begin{pmatrix}\\frac{1}{2}&\\frac{1}{2}\\\\\\frac{1}{2}&\\frac{1}{2}\\end{pmatrix}\\begin{pmatrix}3\\\\1\\end{pmatrix}=\\begin{pmatrix}2\\\\2\\end{pmatrix}',
            'P^2=P',
            '(3,1)^T-(2,2)^T=(1,-1)^T\\perp(1,1)^T',
            'P=\\begin{pmatrix}\\frac{1}{2}&\\frac{1}{2}\\\\\\frac{1}{2}&\\frac{1}{2}\\end{pmatrix}',
            '(2,2)^T',
            'y=x',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
