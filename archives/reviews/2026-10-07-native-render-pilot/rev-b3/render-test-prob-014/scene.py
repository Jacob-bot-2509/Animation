from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'E',
            '\\dfrac{1}{6}',
            '\\dfrac{5}{6}',
            '1+E',
            'E=\\dfrac{1}{6}\\cdot 1+\\dfrac{5}{6}\\cdot(1+E)=1+\\dfrac{5E}{6}',
            'E=6',
            'p=\\dfrac{1}{6}',
            '\\dfrac{1}{p}=6',
            'P(T>k)=(5/6)^k',
            'E[T]=\\sum_{k=0}^\\infty P(T>k)=\\sum_{k=0}^\\infty(5/6)^k=6<\\infty',
            '6',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
