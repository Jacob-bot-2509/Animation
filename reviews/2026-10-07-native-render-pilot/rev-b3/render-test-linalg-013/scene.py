from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'n',
            'D_n=\\begin{vmatrix}1&1&0&\\cdots&0\\\\1&1&1&\\cdots&0\\\\0&1&1&\\cdots&0\\\\\\vdots&&&\\ddots&\\vdots\\\\0&0&\\cdots&1&1\\end{vmatrix}',
            'a_{ii}=a_{i,i+1}=a_{i+1,i}=1',
            'D_n=D_{n-1}-D_{n-2}',
            '1\\cdot D_{n-1}-1\\cdot\\begin{vmatrix}1&1&0&\\cdots\\\\0&1&1&\\cdots\\\\\\vdots\\end{vmatrix}',
            'D_{n-2}',
            'D_1=1',
            'D_2=\\begin{vmatrix}1&1\\\\1&1\\end{vmatrix}=0',
            'D_3=D_2-D_1=-1',
            'D_4=D_3-D_2=-1',
            'D_5=D_4-D_3=0',
            'D_6=D_5-D_4=1',
            '1,0,-1,-1,0,1',
            'D_n=D_{n-6}',
            'D_{n+6}=D_{n+5}-D_{n+4}=\\cdots=D_n',
            'D_{n+2}=D_{n+1}-D_n',
            'D_{n+3}=D_{n+2}-D_{n+1}=-D_n',
            'D_{n+6}=-D_{n+3}=D_n',
            '(1,0),(0,-1),(-1,-1),(-1,0),(0,1),(1,1)',
            'D_1,\\dots,D_6=1,0,-1,-1,0,1',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
