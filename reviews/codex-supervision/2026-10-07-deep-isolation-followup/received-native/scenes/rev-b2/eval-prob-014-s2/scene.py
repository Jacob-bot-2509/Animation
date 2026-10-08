from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'X\\sim\\operatorname{Exp}(\\lambda)',
            '\\lambda>0',
            'P(X>s+t\\mid X>s)=P(X>t)',
            's,t>0',
            'h(t)=\\dfrac{f(t)}{1-F(t)}=\\dfrac{\\lambda e^{-\\lambda t}}{e^{-\\lambda t}}=\\lambda',
            '\\lambda',
            "\\dfrac{F'}{1-F}=\\lambda",
            'F(t)=1-e^{-\\lambda t}',
            'F(0)=0',
            'S=1-F',
            'S^{\\prime}=-\\lambda S',
            'S(0)=1',
            'S(t)=e^{-\\lambda t}',
            'P(X>s+t\\mid X>s)=S(s+t)/S(s)=e^{-\\lambda t}=P(X>t)',
            'h(t)=\\lambda',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
