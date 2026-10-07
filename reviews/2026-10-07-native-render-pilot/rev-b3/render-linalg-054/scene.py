from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\begin{cases} 2x + y = 5 \\\\ x - y = 1 \\end{cases}',
            'D=\\begin{vmatrix} 2 & 1 \\\\ 1 & -1 \\end{vmatrix}=-3\\neq0',
            'D_x=\\begin{vmatrix} 5 & 1 \\\\ 1 & -1 \\end{vmatrix}=-6',
            'D_y=\\begin{vmatrix} 2 & 5 \\\\ 1 & 1 \\end{vmatrix}=-3',
            'x=2, y=1',
            'D=0',
            '2x+y=5',
            'x-y=1',
            '(2,1)',
            'D=-3,\\ D_x=-6,\\ D_y=-3',
            'x=D_x/D=2,\\ y=D_y/D=1',
            'x+y=1,\\ 2x+2y=3',
            'x+y=1,\\ 2x+2y=2',
            '\\{(t,1-t):t\\in\\mathbb R\\}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
