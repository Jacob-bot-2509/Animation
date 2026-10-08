from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'A=\\begin{pmatrix}1&2\\\\2&1\\end{pmatrix}',
            'u=(x+y)/\\sqrt2,\\ v=(x-y)/\\sqrt2',
            'x=(u+v)/\\sqrt2,\\ y=(u-v)/\\sqrt2',
            'x^2+y^2=u^2+v^2',
            '4xy=2u^2-2v^2',
            'f=3u^2-v^2',
            'Q=\\frac1{\\sqrt2}\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}',
            'Q^TAQ=\\operatorname{diag}(3,-1)',
            '3,-1',
            'P=\\sqrt2Q',
            'P^{-1}AP=\\operatorname{diag}(3,-1)',
            '\\lambda_1=3',
            '\\lambda_2=-1',
            '(1,1)^T',
            '(1,-1)^T',
            'P^{-1}AP=\\begin{pmatrix}3&0\\\\0&-1\\end{pmatrix}',
            'P=\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}',
            'x^2+4xy+y^2',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
