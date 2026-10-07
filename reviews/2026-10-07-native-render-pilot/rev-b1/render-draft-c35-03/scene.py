from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'f(x,y)=x^2+2xy+ay^2',
            '1',
            'a',
            'a=0',
            'a=1',
            'a=2',
            'u=x+y,v=y',
            'f=u^2+(a-1)v^2',
            'C=\\begin{pmatrix}1&-1\\\\0&1\\end{pmatrix}',
            'C^{\\mathsf T}AC=\\operatorname{diag}(1,a-1)',
            '\\det C=1',
            'A_{11}=1\\ne0',
            '\\operatorname{rank}A\\ge1',
            '\\det A=a-1',
            'u^2-v^2',
            '(1,1,0)',
            '2',
            'u^2+0v^2',
            '(1,0,1)',
            'u^2+v^2',
            '(2,0,0)',
            'a=1\\iff\\operatorname{rank}A=1',
            'a=0,1,2',
            'u^2-v^2,u^2+0v^2,u^2+v^2',
            '(n_+,n_-,n_0)',
            '(1,1,0),(1,0,1),(2,0,0)',
            'f=x^2+2xy+ay^2',
            'A=\\begin{pmatrix}1&1\\\\1&a\\end{pmatrix}',
            '(x+y)^2-y^2',
            '(x+y)^2',
            '(x+y)^2+y^2',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
