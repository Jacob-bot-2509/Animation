from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'P',
            '\\pi',
            '\\pi=\\pi P',
            'P^T',
            '1',
            'P=\\begin{pmatrix}\\frac12&\\frac12\\\\\\frac14&\\frac34\\end{pmatrix}',
            '\\pi P=\\pi',
            'P^T\\pi^T=\\pi^T',
            '\\pi^T\\ne0',
            '\\pi=(a,b)',
            'a+b=1',
            'a=\\frac12a+\\frac14b',
            'b=2a',
            '\\pi=(\\frac13,\\frac23)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
