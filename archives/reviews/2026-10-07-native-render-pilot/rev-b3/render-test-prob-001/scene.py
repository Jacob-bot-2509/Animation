from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\frac35',
            '\\frac25',
            '\\frac1{50}',
            '\\frac3{100}',
            'A_i',
            'i',
            'D',
            'P(A_1\\cap D)=\\frac35\\cdot\\frac1{50}=\\frac3{250}',
            'P(A_2\\cap D)=\\frac25\\cdot\\frac3{100}=\\frac3{250}',
            'P(D)=\\frac3{125}>0',
            'P(A_1\\mid D)=\\frac{3/250}{3/125}=\\frac12',
            '\\frac12',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
