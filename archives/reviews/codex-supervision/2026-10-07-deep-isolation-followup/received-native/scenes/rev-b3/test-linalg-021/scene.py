from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'A=\\begin{pmatrix}\\cos\\theta&\\sin\\theta\\\\\\sin\\theta&-\\cos\\theta\\end{pmatrix}',
            'A',
            '\\det A=-\\cos^2\\theta-\\sin^2\\theta=-1',
            '\\lambda^2-1=0',
            '\\pm 1',
            '1',
            '\\left(\\cos\\dfrac{\\theta}{2},\\sin\\dfrac{\\theta}{2}\\right)',
            '-1',
            '\\theta=(2k+1)\\pi',
            'x=0',
            '\\tan\\dfrac{\\theta}{2}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
