from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'E_0',
            'E_1',
            'E_0=1+\\dfrac{1}{2}E_0+\\dfrac{1}{2}E_1',
            'E_1=1+\\dfrac{1}{2}\\cdot 0+\\dfrac{1}{2}E_0',
            'E_1=1+\\dfrac{E_0}{2}',
            'E_0=1+\\dfrac{E_0}{2}+\\dfrac{1}{2}\\left(1+\\dfrac{E_0}{2}\\right)=\\dfrac{3}{2}+\\dfrac{3E_0}{4}',
            'E_0=6',
            '1/4',
            'T',
            'P(T>2k)\\le(3/4)^k',
            'E[T]\\le2\\sum_{k=0}^{\\infty}(3/4)^k=8<\\infty',
            '6',
            'E_0=1+\\dfrac12E_0+\\dfrac12E_1',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
