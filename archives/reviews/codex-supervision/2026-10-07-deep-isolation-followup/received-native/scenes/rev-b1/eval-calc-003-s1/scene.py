from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\displaystyle\\lim_{n\\to\\infty}\\left(1+\\frac{1}{n}\\right)^n',
            'e',
            '\\displaystyle\\sum_{k=0}^{\\infty}\\frac{1}{k!}',
            'a_n=\\left(1+\\dfrac{1}{n}\\right)^n',
            'a_n=\\sum_{k=0}^{n}\\binom{n}{k}\\dfrac{1}{n^k}=\\sum_{k=0}^{n}\\dfrac{1}{k!}\\cdot\\dfrac{n(n-1)\\cdots(n-k+1)}{n^k}',
            'a_n',
            'a_{n+1}',
            'k',
            '\\dfrac{n(n-1)\\cdots(n-k+1)}{n^k}\\le\\dfrac{(n+1)n\\cdots(n-k+2)}{(n+1)^k}',
            'a_{n+1}>a_n',
            'a_n\\le\\sum_{k=0}^{n}\\dfrac{1}{k!}\\le 1+1+\\dfrac{1}{2}+\\dfrac{1}{4}+\\cdots+\\dfrac{1}{2^{n-1}}<3',
            '\\lim a_n',
            'E=\\sum_{k=0}^{\\infty}1/k!',
            'k!\\ge2^{k-1}',
            'k\\ge1',
            'a_n=\\sum_{k=0}^{n}c_{k,n}/k!',
            'c_{0,n}=c_{1,n}=1',
            'c_{k,n}=\\prod_{j=0}^{k-1}(1-j/n)\\in[0,1]',
            'm',
            'n\\ge m',
            '\\sum_{k=0}^{m}c_{k,n}/k!\\le a_n\\le E',
            'n\\to\\infty',
            'm\\to\\infty',
            '\\lim a_n=E',
            'e=\\sum_{k=0}^{\\infty}\\frac{1}{k!}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
