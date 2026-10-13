from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\displaystyle S=\\sum_{n=1}^{\\infty}\\frac{n}{2^n}',
            'S=\\dfrac{1}{2}+\\dfrac{2}{4}+\\dfrac{3}{8}+\\dfrac{4}{16}+\\cdots',
            '\\dfrac{S}{2}=\\dfrac{1}{4}+\\dfrac{2}{8}+\\dfrac{3}{16}+\\cdots',
            '\\dfrac{S}{2}=1',
            'S=2',
            'a_n=n/2^n>0',
            'a_{n+1}/a_n=(n+1)/(2n)\\to1/2<1',
            '\\sum_{n=1}^N n/2^n=2-(N+2)/2^N',
            '2',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
