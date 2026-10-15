from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\displaystyle\\sum_{n=0}^{\\infty}\\frac{x^n}{n!}',
            '\\displaystyle\\sum_{n=0}^{\\infty}n!\\,x^n',
            '\\sum_{n=0}^{\\infty}x^n/n!',
            'x\\ne0',
            '|x|/(n+1)\\to0',
            'x',
            '+\\infty',
            '\\sum_{n=0}^{\\infty}n!x^n',
            '(n+1)|x|\\to\\infty',
            'x=0',
            'R=+\\infty',
            'R=0',
            '1/n!',
            'n!',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
