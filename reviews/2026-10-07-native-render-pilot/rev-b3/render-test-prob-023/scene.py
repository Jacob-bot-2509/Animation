from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'd>0',
            '0<l\\le d',
            'X',
            '[0,d/2]',
            '\\Theta',
            '[0,\\pi/2]',
            'x\\sim U\\!\\left(0,\\dfrac{d}{2}\\right)',
            '\\theta\\sim U\\!\\left(0,\\dfrac{\\pi}{2}\\right)',
            'x\\le\\dfrac{l}{2}\\sin\\theta',
            'f(x,\\theta)=\\dfrac{2}{d}\\cdot\\dfrac{2}{\\pi}',
            '\\dfrac{2l}{\\pi d}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
