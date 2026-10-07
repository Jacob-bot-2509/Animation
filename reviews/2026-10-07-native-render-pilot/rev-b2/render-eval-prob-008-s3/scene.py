from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'X\\sim B\\!\\left(100,\\dfrac{1}{2}\\right)',
            'P(|X-50|\\ge 10)',
            'A=\\{|X-50|\\ge10\\}',
            'E((X-50)^2)=25',
            'P(A)\\le1/4',
            'q=2^{-99}\\sum_{k=0}^{40}\\binom{100}{k}',
            '25-100q=E(((X-50)^2-100)\\mathbf1_A)+E((X-50)^2\\mathbf1_{A^c})>0',
            'X=0',
            'q<1/4',
            '\\frac14-q=\\frac{2^{97}-\\sum_{k=0}^{40}\\binom{100}{k}}{2^{99}}>0',
            '\\frac14',
            'E(X)=50',
            '\\operatorname{Var}(X)=25',
            'P(|X-50|\\ge10)\\le1/4',
            '1/4-q=(2^{97}-\\sum_{k=0}^{40}\\binom{100}{k})/2^{99}>0',
            '100',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
