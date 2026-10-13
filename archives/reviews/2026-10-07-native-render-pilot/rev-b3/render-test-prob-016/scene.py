from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'P=\\begin{pmatrix}\\frac45&\\frac15\\\\\\frac25&\\frac35\\end{pmatrix}',
            '1',
            '2',
            '\\pi=(a,b)',
            'a+b=1',
            'a,b\\ge0',
            '\\pi P=\\pi',
            'a=\\frac45a+\\frac25b',
            'a=2b',
            'a=\\frac23',
            'b=\\frac13',
            '(\\frac23,\\frac13)P=(\\frac23,\\frac13)',
            '\\pi=(\\frac23,\\frac13)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
