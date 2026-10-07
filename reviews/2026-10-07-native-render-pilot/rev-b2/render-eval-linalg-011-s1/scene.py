from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\begin{cases}\\lambda x+y+z=1\\\\x+\\lambda y+z=\\lambda\\\\x+y+\\lambda z=\\lambda^2\\end{cases}',
            'D=\\begin{vmatrix}\\lambda&1&1\\\\1&\\lambda&1\\\\1&1&\\lambda\\end{vmatrix}',
            '=(\\lambda-1)I+J',
            'J',
            '(\\lambda-1)+3=\\lambda+2',
            '\\lambda-1',
            'D=(\\lambda+2)(\\lambda-1)^2',
            '\\lambda\\ne 1,-2',
            'D\\ne 0',
            '\\lambda=1',
            'x+y+z=1',
            '\\lambda=-2',
            '0\\cdot(x+y+z)=1+(-2)+4=3',
            '0=3',
            '\\lambda\\ne 1',
            '\\lambda\\ne-2',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
