from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\displaystyle\\int_1^{+\\infty}\\frac{dx}{x^p}',
            'p>0',
            'k\\ge0',
            '[2^k,2^{k+1}]',
            '2^{-p(k+1)}\\le x^{-p}\\le2^{-pk}',
            '2^{-p}2^{(1-p)k}\\le\\int_{2^k}^{2^{k+1}}x^{-p}dx\\le2^{(1-p)k}',
            'p>1',
            '2^{1-p}<1',
            '0<p\\le1',
            '2^{-p}>0',
            'x=e^t',
            '\\int_1^\\infty x^{-p}dx=\\int_0^\\infty e^{-(p-1)t}dt=1/(p-1)',
            '\\dfrac{1}{p-1}',
            '0<p\\le 1',
            '2^{-p}2^{(1-p)k}\\le A_k\\le2^{(1-p)k}',
            'p=1',
            '1/(p-1)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
