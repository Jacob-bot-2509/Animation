from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\begin{vmatrix} a & b \\\\ c & d \\end{vmatrix} = ad - bc',
            'A=\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}',
            'u=(a,c)^T',
            'v=(b,d)^T',
            '0,u,u+v,v',
            '\\det(u,v)=ad-bc',
            '|ad-bc|',
            '\\det A>0',
            '\\det A<0',
            '\\det A=0',
            '\\operatorname{rank}A\\le1',
            '1',
            '0',
            'A=0',
            'ad-bc',
            '\\operatorname{rank}A=1',
            '\\operatorname{rank}A=0',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
