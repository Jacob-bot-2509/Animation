from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'P(1,2,-1)',
            '\\pi:2x-y+2z=3',
            'f(x,y,z)=(x-1)^2+(y-2)^2+(z+1)^2',
            '2x-y+2z-3=0',
            '\\nabla f=\\lambda\\nabla(2x-y+2z-3)',
            '2(x-1)=2\\lambda',
            '2(y-2)=-\\lambda',
            '2(z+1)=2\\lambda',
            'x-1=\\lambda',
            'y-2=-\\dfrac{\\lambda}{2}',
            'z+1=\\lambda',
            '2(1+\\lambda)-\\left(2-\\dfrac{\\lambda}{2}\\right)+2(\\lambda-1)=3',
            '\\dfrac{9\\lambda}{2}-2=3',
            '\\lambda=\\dfrac{10}{9}',
            'd=\\sqrt{\\lambda^2+\\dfrac{\\lambda^2}{4}+\\lambda^2}=\\dfrac{3}{2}|\\lambda|=\\dfrac{5}{3}',
            'Q=(19/9,13/9,1/9)',
            'P-Q',
            'X',
            '(P-Q)\\cdot(X-Q)=0',
            '|P-X|^2=|P-Q|^2+|X-Q|^2=25/9+|X-Q|^2\\ge25/9',
            'X=Q',
            '\\dfrac{5}{3}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
