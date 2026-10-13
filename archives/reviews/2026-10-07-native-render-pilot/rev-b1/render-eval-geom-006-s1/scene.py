from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\pi_1:x+y+z=1',
            '\\pi_2:x-y+z=1',
            '\\pi_3:2x+2z=2',
            '\\begin{pmatrix}1&1&1&1\\\\1&-1&1&1\\\\2&0&2&2\\end{pmatrix}\\to\\begin{pmatrix}1&1&1&1\\\\0&-2&0&0\\\\0&-2&0&0\\end{pmatrix}\\to\\begin{pmatrix}1&1&1&1\\\\0&1&0&0\\\\0&0&0&0\\end{pmatrix}',
            '\\mathrm r(A)=\\mathrm r(\\bar A)=2<3',
            'y=0',
            'x+z=1',
            'y=0,\\ x+z=1',
            '2<3',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
