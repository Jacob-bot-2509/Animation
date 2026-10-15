from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\arctan x',
            '\\dfrac{\\pi}{4}=1-\\dfrac{1}{3}+\\dfrac{1}{5}-\\dfrac{1}{7}+\\cdots',
            'x=1',
            '\\displaystyle\\sum_{n=0}^{\\infty}\\dfrac{(-1)^n}{2n+1}',
            'a_n=\\dfrac{1}{2n+1}\\searrow 0',
            '\\arctan 1=\\dfrac{\\pi}{4}=1-\\dfrac{1}{3}+\\dfrac{1}{5}-\\dfrac{1}{7}+\\cdots',
            'x=-1',
            '1/(1+t^2)=\\sum_{k=0}^{\\infty}(-1)^kt^{2k}',
            '[-r,r]',
            'r<1',
            '0',
            '\\arctan x=\\displaystyle\\sum_{n=0}^{\\infty}\\dfrac{(-1)^n x^{2n+1}}{2n+1}',
            '|x|\\le 1',
            '\\dfrac{\\pi}{4}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
