from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'A=\\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}',
            'A-I=\\begin{pmatrix}0&1\\\\0&0\\end{pmatrix}\\ne 0',
            '(A-I)^2=0',
            'm(\\lambda)=(\\lambda-1)^2',
            '(\\lambda-1)^2',
            '\\iff',
            'A',
            'J_2(1)=\\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}',
            'Av=v',
            '(A-I)(x,y)^T=(y,0)^T=0',
            't(1,0)^T',
            't\\ne0',
            '\\lambda=1',
            't\\ne 0',
            '\\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}',
            '\\operatorname{diag}(1,1)=I',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
