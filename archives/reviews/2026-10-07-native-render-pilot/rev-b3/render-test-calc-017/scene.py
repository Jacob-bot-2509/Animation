from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'f(x,y)=x^2+y^2-xy+x+y',
            'f_x=2x-y+1=0',
            'f_y=2y-x+1=0',
            'x+y+2=0',
            '3x-3y=0',
            'x=y',
            '2x=-2',
            'x=y=-1',
            '(-1,-1)',
            'H=\\begin{pmatrix}2&-1\\\\-1&2\\end{pmatrix}',
            '2>0',
            '\\det H=3>0',
            'f(-1,-1)=1+1-1-1-1=-1',
            'u=x+1,\\ v=y+1',
            'f=-1+u^2+v^2-uv=-1+\\frac12[(u-v)^2+u^2+v^2]',
            'f\\ge-1',
            'u=v=0',
            'y=-1,x\\to\\infty',
            '-1',
            'z=f(x,y)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
