from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'A=\\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}',
            'A^n',
            'n',
            '(x,y)\\mapsto(x+y,y)',
            'n\\ge0',
            '(x+ny,y)',
            'n=0',
            'x+ny',
            'x+(n+1)y',
            'A^n=\\begin{pmatrix}1&n\\\\0&1\\end{pmatrix}',
            'J=A',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
