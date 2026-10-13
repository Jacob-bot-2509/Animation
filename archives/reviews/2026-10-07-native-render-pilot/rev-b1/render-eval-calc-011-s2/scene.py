from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\displaystyle\\sum_{n=1}^{\\infty}\\frac{1}{n\\cdot 2^n}',
            '\\dfrac{1}{n\\cdot 2^n}=\\displaystyle\\int_0^{1/2}x^{n-1}\\,dx',
            '\\dfrac{1}{2^n}',
            'S=\\displaystyle\\sum_{n=1}^{\\infty}\\int_0^{1/2}x^{n-1}dx=\\int_0^{1/2}\\sum_{n=1}^{\\infty}x^{n-1}dx=\\int_0^{1/2}\\dfrac{dx}{1-x}=\\left[-\\ln(1-x)\\right]_0^{1/2}=\\ln 2',
            '\\ln 2',
            '[0,1/2]',
            'x^{n-1}',
            '\\int_0^{1/2}x^{n-1}dx=1/(n2^n)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
