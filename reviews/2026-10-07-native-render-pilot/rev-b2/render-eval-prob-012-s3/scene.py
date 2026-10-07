from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'X,Y',
            'U(0,1)',
            'P(X+Y\\le 1)',
            '(X,Y)',
            '(1-X,1-Y)',
            'X+Y\\le 1\\iff (1-X)+(1-Y)\\ge 1',
            'P(X+Y=1)=0',
            'P(X+Y\\le 1)=P(X+Y\\ge 1)=\\dfrac{1}{2}',
            '\\dfrac{1}{2}',
            '(X,Y)\\sim(1-X,1-Y)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
