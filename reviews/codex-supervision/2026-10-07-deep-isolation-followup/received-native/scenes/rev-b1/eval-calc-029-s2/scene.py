from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'x^{2/3}+y^{2/3}=a^{2/3}',
            'a>0',
            "y'=-\\left(\\dfrac{y}{x}\\right)^{1/3}",
            "ds=\\sqrt{1+(y')^2}\\,dx=\\sqrt{1+(y/x)^{2/3}}\\,dx=\\sqrt{\\dfrac{x^{2/3}+y^{2/3}}{x^{2/3}}}\\,dx",
            'ds=a^{1/3}x^{-1/3}dx',
            'L_1=\\displaystyle\\int_0^a a^{1/3}x^{-1/3}dx=a^{1/3}\\left[\\dfrac{3}{2}x^{2/3}\\right]_0^a=\\dfrac{3a}{2}',
            'L=4L_1=6a',
            'x',
            '0<x\\le a',
            'ds=a^{1/3}x^{-1/3}|dx|',
            'x=0',
            'a',
            'a^{1/3}\\int_0^a x^{-1/3}dx=3a/2',
            '6a',
            "y'=-(y/x)^{1/3}",
            'ds=a^{1/3}x^{-1/3}|dx|\\quad(0<x\\le a)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
