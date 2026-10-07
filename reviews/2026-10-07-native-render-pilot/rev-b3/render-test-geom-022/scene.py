from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'y',
            '\\varphi',
            'R_y(\\varphi)',
            "x'=x\\cos\\varphi+z\\sin\\varphi",
            "y'=y",
            "z'=-x\\sin\\varphi+z\\cos\\varphi",
            'R_y(\\varphi)=\\begin{pmatrix}\\cos\\varphi&0&\\sin\\varphi\\\\0&1&0\\\\-\\sin\\varphi&0&\\cos\\varphi\\end{pmatrix}',
            'R^TR=I',
            '0',
            '\\cos\\varphi\\sin\\varphi-\\sin\\varphi\\cos\\varphi=0',
            '\\cos^2\\varphi+\\sin^2\\varphi=1',
            '1',
            'R',
            '\\det R=1',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
