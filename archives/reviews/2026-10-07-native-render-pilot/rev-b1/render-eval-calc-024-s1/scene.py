from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\arctan x',
            '\\dfrac{\\pi}{4}=1-\\dfrac{1}{3}+\\dfrac{1}{5}-\\dfrac{1}{7}+\\cdots',
            '\\dfrac{1}{1+t}=\\displaystyle\\sum_{n=0}^{\\infty}(-1)^nt^{n}',
            '|t|<1',
            't=x^2',
            '\\dfrac{1}{1+x^2}=\\displaystyle\\sum_{n=0}^{\\infty}(-1)^nx^{2n}',
            '\\arctan x=\\displaystyle\\int_0^x\\dfrac{dt}{1+t^2}=\\sum_{n=0}^{\\infty}(-1)^n\\int_0^xt^{2n}dt=\\sum_{n=0}^{\\infty}\\dfrac{(-1)^nx^{2n+1}}{2n+1}',
            '|x|<1',
            '\\frac1{1+t^2}=\\sum_{k=0}^N(-1)^kt^{2k}+(-1)^{N+1}\\frac{t^{2N+2}}{1+t^2}',
            '0',
            'x\\in[-1,1]',
            '|R_N(x)|\\le|x|^{2N+3}/(2N+3)\\le1/(2N+3)\\to0',
            'x=1',
            '\\pi/4=\\sum_{k=0}^\\infty(-1)^k/(2k+1)',
            '\\arctan x=\\displaystyle\\sum_{n=0}^{\\infty}\\dfrac{(-1)^n x^{2n+1}}{2n+1}',
            '|x|\\le 1',
            '\\dfrac{1}{1+x^2}=\\sum(-1)^nx^{2n}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
