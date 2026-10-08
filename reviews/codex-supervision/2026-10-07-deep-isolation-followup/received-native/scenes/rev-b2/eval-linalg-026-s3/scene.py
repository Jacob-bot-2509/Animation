from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\alpha_1=(1,2,3)',
            '\\alpha_2=(2,3,1)',
            '\\alpha_3=(3,1,2)',
            '|D|=18\\ne 0',
            '\\alpha_2\\times\\alpha_3=(5,-1,-7)',
            '\\alpha_1\\cdot(\\alpha_2\\times\\alpha_3)=5-2-21=-18',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
