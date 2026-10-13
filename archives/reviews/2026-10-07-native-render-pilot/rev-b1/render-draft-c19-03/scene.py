from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'x^2+y^2=1',
            'z=2x',
            'xy',
            '\\begin{cases}x^2+y^2=1\\\\ z=2x\\end{cases}',
            'z',
            '-1\\le x\\le1',
            '(\\cos t,\\sin t,2\\cos t)',
            'e_1=(0,1,0)',
            'e_2=\\frac{(1,0,2)}{\\sqrt5}',
            '(2,0,-1)',
            '\\xi=e_1\\cdot(x,y,z)=y',
            '\\eta=e_2\\cdot(x,y,z)=(x+2z)/\\sqrt5',
            '(\\xi,\\eta)=(\\sin t,\\sqrt5\\cos t)',
            '\\xi^2+\\frac{\\eta^2}{5}=1',
            'y',
            'e_1',
            '1',
            '2',
            '(1,0,2)',
            'e_2',
            '\\sqrt5',
            '2\\sqrt5',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
