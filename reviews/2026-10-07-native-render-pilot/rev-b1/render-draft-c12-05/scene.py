from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'f_n(x)=n^2x(1-x^2)^n',
            '0\\le x\\le1',
            '0',
            '\\int_0^1f_n(x)\\,dx',
            '[0,1]',
            '0<x<1',
            'q=1-x^2<1',
            'n^2q^n',
            'q<1',
            'u=1-x^2',
            '\\int_0^1f_n(x)dx=n^2/[2(n+1)]\\ge n/4\\to\\infty',
            'f_n\\ge0',
            '1',
            '\\sup f_n\\ge\\int f_n\\ge n/4',
            '[a,b]',
            'g_n',
            'g',
            '\\left|\\int_a^b g_n(x)\\,dx-\\int_a^b g(x)\\,dx\\right|\\le(b-a)\\sup_{x\\in[a,b]}|g_n(x)-g(x)|\\to0',
            '\\int_0^1f_n=n^2/[2(n+1)]\\to+\\infty',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
