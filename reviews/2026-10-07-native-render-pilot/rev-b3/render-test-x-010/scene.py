from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\sigma_1,\\sigma_2>0',
            '\\begin{pmatrix}\\sigma_1^2&\\rho\\sigma_1\\sigma_2\\\\\\rho\\sigma_1\\sigma_2&\\sigma_2^2\\end{pmatrix}',
            '|\\rho|<1',
            '\\sigma_1^2>0',
            '\\sigma_1^2\\sigma_2^2(1-\\rho^2)',
            '\\iff',
            '\\iff 1-\\rho^2>0\\iff|\\rho|<1',
            'X-E[X]',
            'Y-E[Y]',
            'a,b',
            'aX+bY',
            '\\iff|\\rho|<1',
            '\\rho=\\pm 1',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
