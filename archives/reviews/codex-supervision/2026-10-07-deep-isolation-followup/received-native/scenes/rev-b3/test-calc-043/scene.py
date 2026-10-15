from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\displaystyle\\int_0^{+\\infty}e^{-x^2}\\,dx',
            'I_R=\\int_0^R e^{-x^2}dx',
            'I_R^2=\\iint_{[0,R]^2}e^{-(x^2+y^2)}dxdy',
            'R',
            '\\sqrt2R',
            'r',
            'J_r=\\int_0^{\\pi/2}\\int_0^r e^{-u^2}u\\,du\\,d\\theta=\\frac{\\pi}{4}(1-e^{-r^2})',
            '\\frac{\\pi}{4}(1-e^{-R^2})\\le I_R^2\\le\\frac{\\pi}{4}(1-e^{-2R^2})',
            'I_R>0',
            '\\pi/4',
            '\\int_0^\\infty e^{-x^2}dx=\\sqrt\\pi/2',
            '\\dfrac{\\sqrt\\pi}{2}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
