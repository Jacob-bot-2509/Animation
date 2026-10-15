from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'C_i',
            'i',
            'H_2',
            'P(H_2|C_3)=1',
            'P(H_2|C_1)=\\dfrac{1}{2}',
            'P(H_2|C_2)=0',
            'P(C_i)=\\dfrac{1}{3}',
            'P(C_3|H_2)=\\dfrac{P(H_2|C_3)P(C_3)}{P(H_2|C_3)P(C_3)+P(H_2|C_1)P(C_1)+P(H_2|C_2)P(C_2)}=\\dfrac{1\\cdot\\frac{1}{3}}{1\\cdot\\frac{1}{3}+\\frac{1}{2}\\cdot\\frac{1}{3}+0}=\\dfrac{1/3}{1/2}=\\dfrac{2}{3}',
            '\\dfrac{2}{3}',
            '\\dfrac{1}{3}',
            'P(C_3|H_2)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
