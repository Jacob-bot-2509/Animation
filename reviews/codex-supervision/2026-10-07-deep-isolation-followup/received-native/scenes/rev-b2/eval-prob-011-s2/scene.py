from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\{0,1,H\\}',
            'H',
            'P=\\begin{pmatrix}1/2&1/2&0\\\\1/2&0&1/2\\\\0&0&1\\end{pmatrix}',
            'Q=\\begin{pmatrix}1/2&1/2\\\\1/2&0\\end{pmatrix}',
            'N=(I-Q)^{-1}=\\begin{pmatrix}1/2&-1/2\\\\-1/2&1\\end{pmatrix}^{-1}=4\\begin{pmatrix}1&1/2\\\\1/2&1/2\\end{pmatrix}=\\begin{pmatrix}4&2\\\\2&2\\end{pmatrix}',
            '\\det(I-Q)=\\dfrac{1}{2}-\\dfrac{1}{4}=\\dfrac{1}{4}',
            'N',
            '=4+2=6',
            '1/4',
            'T',
            'P(T>2k)\\le(3/4)^k',
            'E[T]\\le2\\sum_{k=0}^{\\infty}(3/4)^k=8<\\infty',
            '6',
            'N=(I-Q)^{-1}=\\begin{pmatrix}4&2\\\\2&2\\end{pmatrix}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
