from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'A=\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}',
            '\\det A',
            'A',
            'A^{-1}',
            '\\det A=-2\\ne 0',
            '\\operatorname{rank}A=2',
            'AA^{-1}=\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}\\begin{pmatrix}-2&1\\\\\\frac{3}{2}&-\\frac{1}{2}\\end{pmatrix}=\\begin{pmatrix}-2+3&1-1\\\\-6+6&3-2\\end{pmatrix}=\\begin{pmatrix}1&0\\\\0&1\\end{pmatrix}',
            '\\det A=-2',
            '2',
            'A^{-1}=\\begin{pmatrix}-2&1\\\\\\frac{3}{2}&-\\frac{1}{2}\\end{pmatrix}',
            '-2',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
