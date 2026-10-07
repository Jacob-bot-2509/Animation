from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'l_1:\\dfrac{x-1}{2}=\\dfrac{y+1}{1}=\\dfrac{z-2}{-1}',
            'l_2:\\dfrac{x+1}{1}=\\dfrac{y-2}{2}=\\dfrac{z}{1}',
            'd_1=(2,1,-1)',
            'd_2=(1,2,1)',
            'd_1\\times d_2=(3,-3,3)\\ne0',
            '\\Delta=(-2,3,-2)',
            '-21\\ne0',
            '\\Delta',
            '\\operatorname{span}\\{d_1,d_2\\}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
