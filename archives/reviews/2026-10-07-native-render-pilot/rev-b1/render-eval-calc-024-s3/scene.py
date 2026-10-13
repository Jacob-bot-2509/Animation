from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\arctan x',
            '\\dfrac{\\pi}{4}=1-\\dfrac{1}{3}+\\dfrac{1}{5}-\\dfrac{1}{7}+\\cdots',
            'f(x)=\\arctan x',
            'f^{(n)}(0)',
            "f'(x)=\\dfrac{1}{1+x^2}",
            '\\arctan',
            '|f^{(m)}(t)|\\le(m-1)!',
            'm\\ge 1',
            't',
            '|R_N(x)|=\\dfrac{|f^{(N+1)}(\\xi)|}{(N+1)!}|x|^{N+1}\\le\\dfrac{N!}{(N+1)!}\\cdot 1=\\dfrac{1}{N+1}\\to 0',
            '|x|\\le 1',
            'm\\ge1',
            'f^{(m)}(t)=\\frac{(-1)^{m-1}(m-1)!}{2i}[(t-i)^{-m}-(t+i)^{-m}]',
            '|f^{(m)}(t)|\\le(m-1)!(1+t^2)^{-m/2}\\le(m-1)!',
            'f^{(2k+1)}(0)=(-1)^k(2k)!',
            'f^{(2k)}(0)=0',
            '1/(N+1)',
            '\\arctan x=\\displaystyle\\sum_{n=0}^{\\infty}\\dfrac{(-1)^n x^{2n+1}}{2n+1}',
            'x=1',
            '\\dfrac{1}{N+1}\\to0',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
