from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\displaystyle\\int_1^{+\\infty}\\frac{dx}{x^p}',
            'p>0',
            'p\\ne 1',
            '\\displaystyle\\int_1^b x^{-p}dx=\\left[\\dfrac{x^{1-p}}{1-p}\\right]_1^b=\\dfrac{b^{1-p}-1}{1-p}',
            'p>1',
            '1-p<0',
            'b^{1-p}\\to 0',
            '\\dfrac{0-1}{1-p}=\\dfrac{1}{p-1}',
            '0<p<1',
            'b^{1-p}\\to+\\infty',
            'p=1',
            '\\displaystyle\\int_1^b\\dfrac{dx}{x}=\\ln b\\to+\\infty',
            '\\dfrac{1}{p-1}',
            '0<p\\le 1',
            'p\\ne1',
            '(b^{1-p}-1)/(1-p)',
            '\\ln b',
            '1/(p-1)',
            '0<p\\le1',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
