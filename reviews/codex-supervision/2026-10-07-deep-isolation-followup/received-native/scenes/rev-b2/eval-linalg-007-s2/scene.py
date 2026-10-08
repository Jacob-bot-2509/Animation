from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'A=\\begin{pmatrix}\\cos\\theta&-\\sin\\theta\\\\\\sin\\theta&\\cos\\theta\\end{pmatrix}',
            'A^n',
            'n\\in\\mathbb Z_{\\ge0}',
            'n=0',
            'A^0=I',
            '(\\cos\\theta-\\lambda)^2+\\sin^2\\theta=0',
            '\\lambda^2-2\\lambda\\cos\\theta+1=0',
            '\\lambda=e^{\\pm i\\theta}',
            '(1,\\mp i)^T',
            'P=\\begin{pmatrix}1&1\\\\-i&i\\end{pmatrix}',
            'P^{-1}=\\dfrac{1}{2}\\begin{pmatrix}1&i\\\\1&-i\\end{pmatrix}',
            'A=P\\begin{pmatrix}e^{i\\theta}&0\\\\0&e^{-i\\theta}\\end{pmatrix}P^{-1}',
            'e^{\\pm in\\theta}=\\cos n\\theta\\pm i\\sin n\\theta',
            'A^n=\\begin{pmatrix}\\cos n\\theta&-\\sin n\\theta\\\\\\sin n\\theta&\\cos n\\theta\\end{pmatrix}',
            'e^{\\pm i\\theta}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
