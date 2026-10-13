from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'A=\\begin{pmatrix}0&1\\\\0&0\\end{pmatrix}',
            'e^{tA}',
            't',
            '(sI-A)^{-1}=\\begin{pmatrix}s&-1\\\\0&s\\end{pmatrix}^{-1}=\\dfrac{1}{s^2}\\begin{pmatrix}s&1\\\\0&s\\end{pmatrix}=\\begin{pmatrix}1/s&1/s^2\\\\0&1/s\\end{pmatrix}',
            '\\mathcal L^{-1}\\{1/s\\}=1',
            '\\mathcal L^{-1}\\{1/s^2\\}=t',
            'e^{tA}=\\begin{pmatrix}1&t\\\\0&1\\end{pmatrix}',
            't\\ge0',
            '\\Phi(t)=I+tA',
            '\\Phi^{\\prime}=A\\Phi',
            '\\Phi(0)=I',
            '\\Phi(t)=e^{tA}',
            '(sI-A)^{-1}=\\begin{pmatrix}1/s&1/s^2\\\\0&1/s\\end{pmatrix}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
