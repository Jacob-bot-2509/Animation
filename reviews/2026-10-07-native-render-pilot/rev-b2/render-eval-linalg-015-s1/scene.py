from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'A=\\begin{pmatrix}1&2\\\\2&1\\end{pmatrix}',
            '|\\lambda I-A|=\\begin{vmatrix}\\lambda-1&-2\\\\-2&\\lambda-1\\end{vmatrix}=(\\lambda-1)^2-4=\\lambda^2-2\\lambda-3=(\\lambda-3)(\\lambda+1)',
            '\\lambda=3,-1',
            '\\lambda=3',
            '(3I-A)v=0',
            '\\begin{pmatrix}2&-2\\\\-2&2\\end{pmatrix}v=0',
            'v=(1,1)^T',
            '\\lambda=-1',
            '(-I-A)v=0',
            '\\begin{pmatrix}-2&-2\\\\-2&-2\\end{pmatrix}v=0',
            'v=(1,-1)^T',
            'P=((1,1)^T,(1,-1)^T)=\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}',
            '\\det P=-2\\ne0',
            'AP=P\\operatorname{diag}(3,-1)',
            'P^{-1}AP=\\operatorname{diag}(3,-1)',
            '\\lambda_1=3',
            '\\lambda_2=-1',
            '(1,1)^T',
            '(1,-1)^T',
            'P^{-1}AP=\\begin{pmatrix}3&0\\\\0&-1\\end{pmatrix}',
            'P=\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}',
            '(\\lambda-3)(\\lambda+1)=0',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
