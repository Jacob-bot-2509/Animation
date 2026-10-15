from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'z = x^2 + y^2',
            '(x_0, y_0, z_0)',
            '(l, m, n)',
            '(x_0+lt, y_0+mt, z_0+nt)',
            'z=x^2+y^2',
            't^2(l^2+m^2)+t(2x_0l+2y_0m-n)+(x_0^2+y_0^2-z_0)=0',
            't',
            'l^2+m^2=0',
            'l=m=0',
            '2x_0l+2y_0m-n=0',
            'n=0',
            '(x,y,z)=(x_0+lt,y_0+mt,z_0+nt)',
            '(l,m,n)\\ne(0,0,0)',
            't\\in\\mathbb R',
            '-n=0',
            '(l,m,n)=(0,0,0)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
