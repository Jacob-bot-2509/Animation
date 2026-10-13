from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\displaystyle\\int_1^{+\\infty}\\frac{dx}{x^p}',
            'p>0',
            'f(x)=x^{-p}',
            '[1,+\\infty)',
            '\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{1}{n^p}',
            '\\displaystyle\\int_1^{+\\infty}\\dfrac{dx}{x^p}',
            'p>1',
            'p\\le 1',
            '\\int_1^b x^{-p}dx=(b^{1-p}-1)/(1-p)',
            'p\\ne1',
            'b^{1-p}\\to0',
            '1/(p-1)',
            'p=1',
            '\\ln b\\to\\infty',
            '\\dfrac{1}{p-1}',
            '0<p\\le 1',
            'y=\\dfrac{1}{x^p}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
