from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'E',
            '\\dfrac{1}{2}',
            '1+E',
            'E=\\dfrac{1}{2}\\cdot 1+\\dfrac{1}{2}\\cdot(1+E)=1+\\dfrac{E}{2}',
            'E=2',
            'X',
            'P(X>2k)=4^{-k}',
            'E[X]\\le2\\sum_{k=0}^{\\infty}4^{-k}=8/3<\\infty',
            'E[X]=2',
            '2',
            'E=1+\\dfrac{E}{2}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
