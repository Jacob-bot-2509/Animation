from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'X\\sim\\operatorname{Exp}(1)',
            'E[X^n]=n!',
            'n\\in\\mathbb Z_{\\ge0}',
            'n\\in\\{0,1,2,\\dots\\}',
            'E[X^n]=\\displaystyle\\int_0^{\\infty}x^ne^{-x}dx',
            'I_n=\\displaystyle\\int_0^{\\infty}x^ne^{-x}dx',
            'I_0=\\displaystyle\\int_0^{\\infty}e^{-x}dx=1',
            'n\\ge 1',
            'u=x^n',
            'dv=e^{-x}dx',
            'I_n=\\left[-x^ne^{-x}\\right]_0^{\\infty}+n\\displaystyle\\int_0^{\\infty}x^{n-1}e^{-x}dx=nI_{n-1}',
            'x^ne^{-x}\\big|_0^\\infty',
            'I_n=n!',
            '\\Gamma(n+1)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
