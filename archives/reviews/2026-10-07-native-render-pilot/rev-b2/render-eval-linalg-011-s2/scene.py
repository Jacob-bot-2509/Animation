from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\begin{cases}\\lambda x+y+z=1\\\\x+\\lambda y+z=\\lambda\\\\x+y+\\lambda z=\\lambda^2\\end{cases}',
            '\\begin{pmatrix}1&1&\\lambda&\\lambda^2\\\\0&\\lambda-1&1-\\lambda&\\lambda-\\lambda^2\\\\0&1-\\lambda&1-\\lambda^2&1-\\lambda^3\\end{pmatrix}',
            '\\lambda\\ne1',
            '\\lambda-1',
            '(0,1,-1,-\\lambda)',
            '(1-\\lambda)',
            '(0,0,(1-\\lambda)(\\lambda+2),(1-\\lambda)(\\lambda+1)^2)',
            '\\lambda\\ne1,-2',
            '\\lambda=-2',
            '0=3',
            '\\lambda=1',
            'x+y+z=1',
            '\\lambda\\ne 1',
            '\\lambda\\ne-2',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
