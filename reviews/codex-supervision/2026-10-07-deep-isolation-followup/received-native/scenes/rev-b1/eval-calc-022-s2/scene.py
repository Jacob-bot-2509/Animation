from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\displaystyle S=\\sum_{n=1}^{\\infty}\\frac{n^2}{2^n}',
            'A=\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{n}{2^n}=2',
            'B=\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{1}{2^n}=1',
            '\\dfrac{S}{2}=\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{n^2}{2^{n+1}}=\\sum_{m=2}^{\\infty}\\dfrac{(m-1)^2}{2^m}',
            'S-\\dfrac{S}{2}=\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{n^2-(n-1)^2}{2^n}=\\sum_{n=1}^{\\infty}\\dfrac{2n-1}{2^n}=2A-B=2\\cdot 2-1=3',
            '\\dfrac{S}{2}=3',
            'S=6',
            'a_{n+1}/a_n=(n+1)^2/(2n^2)\\to1/2<1',
            '\\sum_{n=1}^N n^2/2^n=6-(N^2+4N+6)/2^N',
            '6',
            'A=2',
            'B=1',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
