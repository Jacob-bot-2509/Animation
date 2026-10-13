from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'X\\sim B\\!\\left(10,\\dfrac{3}{10}\\right)',
            'P(X=3)',
            'P(X\\le 1)',
            'P(X=3)=\\binom{10}{3}\\left(\\frac3{10}\\right)^3\\left(\\frac7{10}\\right)^7=\\frac{120\\cdot3^3\\cdot7^7}{10^{10}}=\\frac{66706983}{250000000}',
            'P(X\\le1)=P(X=0)+P(X=1)=\\left(\\frac7{10}\\right)^{10}+10\\cdot\\frac3{10}\\left(\\frac7{10}\\right)^9=\\frac{7^{10}+30\\cdot7^9}{10^{10}}=\\frac{1493083459}{10000000000}',
            'P(X=3)=\\frac{66706983}{250000000}',
            'P(X\\le1)=\\frac{1493083459}{10000000000}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
