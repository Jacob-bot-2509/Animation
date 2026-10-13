from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'M=\\begin{pmatrix}2&1&1\\\\1&2&1\\\\0&0&3\\end{pmatrix}',
            '\\det M=(-1)^{3+3}\\cdot 3\\cdot\\begin{vmatrix}2&1\\\\1&2\\end{vmatrix}=3\\cdot 3=9',
            '2\\times2',
            'B=\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}',
            'C=(3)',
            '\\det M=\\det B\\det C=3\\cdot3=9',
            '9',
            '(-1)^{3+3}\\cdot3',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
