from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'x_1+x_2+x_3+x_4=0',
            '\\mathbb R^4',
            '(1,1,1,1)',
            '4-1=3',
            '\\xi_1=(1,-1,0,0)^T,\\xi_2=(1,0,-1,0)^T,\\xi_3=(1,0,0,-1)^T',
            'x',
            'x_1=-x_2-x_3-x_4',
            'x=-x_2\\xi_1-x_3\\xi_2-x_4\\xi_3',
            '\\xi_1=(1,-1,0,0)^T',
            '\\xi_2=(1,0,-1,0)^T',
            '\\xi_3=(1,0,0,-1)^T',
            'x=c_1\\xi_1+c_2\\xi_2+c_3\\xi_3',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
