from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\sum_{n=1}^{\\infty} \\frac{(-1)^n}{\\sqrt{n}}',
            'u_n=1/\\sqrt n',
            'u_{n+1}\\le u_n',
            '\\lim_{n\\to\\infty}u_n=0',
            '\\sum_{n=1}^{\\infty}(-1)^n u_n',
            'S',
            'N',
            'S_N',
            '|S-S_N|\\le 1/\\sqrt{N+1}',
            '\\sum_{n=1}^{N}1/\\sqrt n\\ge\\int_1^{N+1}x^{-1/2}\\,dx=2(\\sqrt{N+1}-1)\\to+\\infty',
            'p=\\frac{1}{2}\\le1',
            'p',
            'u_n\\downarrow0',
            '|S-S_N|\\le1/\\sqrt{N+1}',
            '\\sum_{n=1}^Nn^{-1/2}\\ge\\int_1^{N+1}x^{-1/2}\\,dx=2(\\sqrt{N+1}-1)\\to+\\infty',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
