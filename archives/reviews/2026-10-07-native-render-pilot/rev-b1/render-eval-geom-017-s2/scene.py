from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\vec a=(1,2,2)',
            '\\vec b=(-2,1,2)',
            '\\vec a',
            '\\vec b',
            '|\\vec a|\\cos\\theta=3\\cdot\\dfrac{4}{9}=\\dfrac{4}{3}',
            '\\dfrac{\\vec b}{|\\vec b|}=\\dfrac{1}{3}(-2,1,2)',
            '=\\dfrac{4}{3}\\cdot\\dfrac{1}{3}(-2,1,2)=\\left(-\\dfrac{8}{9},\\dfrac{4}{9},\\dfrac{8}{9}\\right)',
            '|\\vec a-\\vec b|^2=|(3,1,0)|^2=10',
            '|\\vec a|=|\\vec b|=3',
            '\\cos\\theta=(9+9-10)/(2\\cdot3\\cdot3)=4/9',
            '\\cos\\theta=\\dfrac{4}{9}',
            '\\left(-\\dfrac{8}{9},\\dfrac{4}{9},\\dfrac{8}{9}\\right)',
            '\\dfrac{4}{3}',
            '\\dfrac{\\vec b}{3}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
