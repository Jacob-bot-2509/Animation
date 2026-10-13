from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'a',
            '\\begin{cases}ax+y+z=0\\\\x+ay+z=0\\\\x+y+az=0\\end{cases}',
            '(a-1)I+J',
            '(a-1)^2(a+2)',
            'a\\ne1,-2',
            'a=1',
            'x+y+z=0',
            'a=-2',
            '4-1=3\\ne0',
            '-3x+3y=0',
            'z=x',
            '\\operatorname{span}\\{(1,1,1)^T\\}',
            'x=y=z',
            '3-r',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
