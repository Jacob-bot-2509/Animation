from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\displaystyle\\lim_{n\\to\\infty}\\left(1+\\frac{1}{n}\\right)^n',
            'e',
            '\\displaystyle\\sum_{k=0}^{\\infty}\\frac{1}{k!}',
            'n\\ln\\left(1+\\dfrac{1}{n}\\right)=\\dfrac{\\ln(1+x)}{x}',
            'x=\\dfrac{1}{n}\\to 0^+',
            '\\lim_{x\\to 0^+}\\dfrac{\\ln(1+x)}{x}=\\lim_{x\\to 0^+}\\dfrac{1}{1+x}=1',
            '\\lim n\\ln(1+1/n)=1',
            '=e^1',
            'E(x)=\\sum_{k=0}^{\\infty}x^k/k!',
            'E^{\\prime}=E',
            'E(0)=1',
            '(e^{-x}E(x))^{\\prime}=0',
            'E(x)=e^x',
            'e=\\sum_{k=0}^{\\infty}1/k!',
            'e=\\sum_{k=0}^{\\infty}\\frac{1}{k!}',
            'y=\\dfrac{\\ln(1+x)}{x}',
            'x\\to0^+',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
