from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'A=\\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}',
            'x^2+y^2=1',
            'A',
            '(x,y)',
            "(x',y')=(x+y,y)",
            "x=x'-y'",
            "y=y'",
            "(x'-y')^2+y'^2=1",
            "x'^2-2x'y'+2y'^2=1",
            "x'^2-2x'y'+2y'^2",
            '\\begin{pmatrix}1&-1\\\\-1&2\\end{pmatrix}',
            '1>0',
            '\\det A=1',
            '=\\pi\\cdot|\\det A|=\\pi',
            'x^2-2xy+2y^2=1',
            '\\pi',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
