from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '(1,2),(2,4),(3,7)',
            'y=ax+b',
            'A=\\begin{pmatrix}1&1\\\\2&1\\\\3&1\\end{pmatrix}',
            '\\vec b=(2,4,7)^T',
            'A^TA\\vec x=A^T\\vec b',
            'A^TA=\\begin{pmatrix}14&6\\\\6&3\\end{pmatrix}',
            'A^T\\vec b=\\begin{pmatrix}31\\\\13\\end{pmatrix}',
            '\\begin{cases}14a+6b=31\\\\6a+3b=13\\end{cases}',
            '2a+b=\\dfrac{13}{3}',
            'b=\\dfrac{13}{3}-2a',
            '14a+6\\left(\\dfrac{13}{3}-2a\\right)=31',
            '14a+26-12a=31',
            '2a=5',
            'a=\\dfrac{5}{2}',
            'b=\\dfrac{13}{3}-5=-\\dfrac{2}{3}',
            'y=\\dfrac{5}{2}x-\\dfrac{2}{3}',
            'x=1,2,3',
            '\\dfrac{11}{6},\\dfrac{13}{3},\\dfrac{41}{6}',
            '\\left(\\dfrac{1}{6}\\right)^2+\\left(-\\dfrac{1}{3}\\right)^2+\\left(\\dfrac{1}{6}\\right)^2=\\dfrac{1}{6}',
            'c_*=(5/2,-2/3)^T',
            'r=b-Ac_*=(1/6,-1/3,1/6)^T',
            'A^Tr=0',
            'c=c_*+\\delta',
            '\\|b-Ac\\|^2=\\|r\\|^2+\\|A\\delta\\|^2\\ge1/6',
            'A',
            '\\det(A^TA)=6>0',
            '\\delta=0',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
