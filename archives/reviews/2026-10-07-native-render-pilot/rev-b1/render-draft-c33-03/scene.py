from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'M=\\begin{pmatrix}2&1&1\\\\1&1&0\\\\0&0&2\\end{pmatrix}',
            'M',
            '\\begin{pmatrix}A&b\\\\0&d\\end{pmatrix}',
            'A=\\begin{pmatrix}2&1\\\\1&1\\end{pmatrix}',
            'b=\\begin{pmatrix}1\\\\0\\end{pmatrix}',
            'd=2',
            'A',
            'A^{-1}=\\begin{pmatrix}1&-1\\\\-1&2\\end{pmatrix}',
            'M^{-1}=\\begin{pmatrix}A^{-1}&-\\frac{1}{d}A^{-1}b\\\\0&\\frac{1}{d}\\end{pmatrix}',
            'A^{-1}b=\\begin{pmatrix}1\\\\-1\\end{pmatrix}',
            '-\\frac12A^{-1}b=\\begin{pmatrix}-\\frac12\\\\\\frac12\\end{pmatrix}',
            'M^{-1}=\\begin{pmatrix}1&-1&-\\frac12\\\\-1&2&\\frac12\\\\0&0&\\frac12\\end{pmatrix}',
            'MM^{-1}=I',
            'M^{-1}',
            '(A\\ b;0\\ d)',
            'd',
            'A^{-1}',
            'A^{-1}b',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
