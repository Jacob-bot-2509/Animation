from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\displaystyle S=\\sum_{n=1}^{\\infty}\\frac{n^2}{2^n}',
            '\\displaystyle\\sum_{n=1}^{\\infty}x^n=\\dfrac{x}{1-x}',
            '\\displaystyle\\sum_{n=1}^{\\infty}nx^{n-1}=\\dfrac{1}{(1-x)^2}',
            '\\displaystyle\\sum_{n=1}^{\\infty}n(n-1)x^{n-2}=\\dfrac{2}{(1-x)^3}',
            '\\displaystyle\\sum_{n=1}^{\\infty}n^2x^n=\\sum_{n=1}^{\\infty}n(n-1)x^n+\\sum_{n=1}^{\\infty}nx^n=\\dfrac{2x^2}{(1-x)^3}+\\dfrac{x}{(1-x)^2}=\\dfrac{x(1+x)}{(1-x)^3}',
            'x=\\dfrac{1}{2}',
            'S=\\dfrac{(1/2)(3/2)}{(1/2)^3}=6',
            '6',
            '\\sum_{n=1}^{\\infty}n^2x^n=\\dfrac{x(1+x)}{(1-x)^3}\\quad(|x|<1)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
