from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'b_1,b_2,b_3\\in\\mathbb Z',
            '\\begin{cases}x+y+z=b_1\\\\x-y+z=b_2\\\\x+y-z=b_3\\end{cases}',
            '(x,y,z)\\in\\mathbb Z^3',
            'A=\\begin{pmatrix}1&1&1\\\\1&-1&1\\\\1&1&-1\\end{pmatrix}',
            'D=\\det A=4\\ne0',
            '\\mathbb Q^3',
            'D_x=2(b_2+b_3)',
            'D_y=2(b_1-b_2)',
            'D_z=2(b_1-b_3)',
            'x=\\frac{b_2+b_3}{2}',
            'y=\\frac{b_1-b_2}{2}',
            'z=\\frac{b_1-b_3}{2}',
            'x,y,z\\in\\mathbb Z',
            'b_1-b_2=2y',
            'b_1-b_3=2z',
            'b_1\\equiv b_2\\equiv b_3\\pmod2',
            'b_1,b_2,b_3',
            '\\det A\\ne0',
            'A\\mathbb Z^3=\\{b\\in\\mathbb Z^3:b_1\\equiv b_2\\equiv b_3\\pmod2\\}',
            '(b_1-b_2,b_1-b_3)\\bmod2',
            '4',
            '\\mathbb Z^3',
            '(x,y,z)=\\left(\\frac{b_2+b_3}{2},\\frac{b_1-b_2}{2},\\frac{b_1-b_3}{2}\\right)',
            'b\\in\\mathbb Z^3',
            '\\det A=4',
            '\\frac{b_2+b_3}{2},\\frac{b_1-b_2}{2},\\frac{b_1-b_3}{2}',
            'A\\mathbb Z^3',
            'D=4',
            'D_x,D_y,D_z',
            'D\\ne0',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
