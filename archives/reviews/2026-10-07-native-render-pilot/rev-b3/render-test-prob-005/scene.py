from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'X,Y',
            'U(0,1)',
            'Z=X+Y',
            'P(Z>\\frac32)',
            'f_Z(z)=\\int_{\\mathbb R}\\mathbf1_{(0,1)}(x)\\mathbf1_{(0,1)}(z-x)\\,dx',
            'f_Z(z)=\\begin{cases}z,&0<z<1,\\\\2-z,&1\\le z<2,\\\\0,&\\text{其他}.\\end{cases}',
            'P(Z>\\frac32)=\\int_{3/2}^2(2-z)\\,dz=[2z-z^2/2]_{3/2}^2=2-\\frac{15}{8}=\\frac18',
            'P(Z>\\frac32)=\\frac18',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
