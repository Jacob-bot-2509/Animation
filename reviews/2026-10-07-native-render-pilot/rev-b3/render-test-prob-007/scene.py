from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'T\\sim\\operatorname{Exp}\\!\\left(\\dfrac{1}{1000}\\right)',
            '\\lambda=\\dfrac{1}{1000}',
            'P(T>1500\\mid T>500)',
            'P(T>t)=e^{-t/1000}',
            't\\ge0',
            '\\{T>1500\\}\\subseteq\\{T>500\\}',
            'P(T>1500\\mid T>500)=\\frac{e^{-1500/1000}}{e^{-500/1000}}=\\frac{e^{-3/2}}{e^{-1/2}}=e^{-1}',
            'e^{-1}',
            'S(t)=P(T>t)=e^{-t/1000}',
            'P(T>500+t\\mid T>500)=S(500+t)/S(500)=S(t)',
            'S(500+t)=e^{-1/2}S(t)',
            'S(t)',
            't=1000',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
