from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'n=3',
            'D=\\begin{vmatrix}a+b&a&a\\\\a&a+b&a\\\\a&a&a+b\\end{vmatrix}',
            'n',
            'A=bI+aJ',
            'J',
            'n,0,\\dots,0',
            'J(1,\\dots,1)^T=n(1,\\dots,1)^T',
            'A',
            'b+na',
            'b',
            'n-1',
            'D=(b+3a)\\cdot b\\cdot b=b^2(3a+b)',
            'D_n=b^{n-1}(na+b)',
            'b^2(3a+b)',
            'b^{n-1}(na+b)',
            'bI+aJ',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
