from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\begin{cases}\\lambda x+y+z=1\\\\x+\\lambda y+z=\\lambda\\\\x+y+\\lambda z=\\lambda^2\\end{cases}',
            '\\lambda=1',
            'x+y+z=1',
            '\\lambda=-2',
            '(\\lambda-1)I+J',
            '(\\lambda-1)^2(\\lambda+2)',
            '\\lambda\\ne1,-2',
            '1-2+4=3',
            '(1,1,1)',
            '\\lambda\\ne 1',
            '\\lambda\\ne-2',
            '\\lambda',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
