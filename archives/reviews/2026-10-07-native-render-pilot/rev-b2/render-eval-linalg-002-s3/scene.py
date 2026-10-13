from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'D=\\begin{vmatrix}1&1&1&1\\\\1&2&1&1\\\\1&1&3&1\\\\1&1&1&4\\end{vmatrix}',
            '\\begin{vmatrix}0&0&0&-3\\\\0&1&0&-3\\\\0&0&2&-3\\\\1&1&1&4\\end{vmatrix}',
            'D=(-1)^{4+1}\\cdot 1\\cdot\\begin{vmatrix}0&0&-3\\\\1&0&-3\\\\0&2&-3\\end{vmatrix}=-\\left[0-0+(-3)\\begin{vmatrix}1&0\\\\0&2\\end{vmatrix}\\right]=-(-3\\cdot 2)=6',
            '6',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
