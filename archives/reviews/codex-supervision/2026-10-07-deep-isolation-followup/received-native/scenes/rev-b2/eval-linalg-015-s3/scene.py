from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'A=\\begin{pmatrix}1&2\\\\2&1\\end{pmatrix}',
            'q_1=\\dfrac{1}{\\sqrt2}(1,1)^T',
            'q_2=\\dfrac{1}{\\sqrt2}(1,-1)^T',
            'Q=\\dfrac{1}{\\sqrt2}\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}',
            'Q',
            'Q^{-1}=Q^T',
            'Q^TAQ=\\begin{pmatrix}3&0\\\\0&-1\\end{pmatrix}',
            '\\lambda_1=3',
            '\\lambda_2=-1',
            '(1,1)^T',
            '(1,-1)^T',
            'P^{-1}AP=\\begin{pmatrix}3&0\\\\0&-1\\end{pmatrix}',
            'P=\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}',
            '\\det Q=-1',
            'Q^TAQ=\\operatorname{diag}(3,-1)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
