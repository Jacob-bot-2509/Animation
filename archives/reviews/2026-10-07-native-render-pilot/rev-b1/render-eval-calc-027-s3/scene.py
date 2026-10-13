from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\displaystyle I=\\int_0^1\\!\\!\\int_x^1 e^{y^2}\\,dy\\,dx',
            'D=\\{(x,y):0\\le x\\le y\\le1\\}',
            'I=\\int_0^1\\int_0^y e^{y^2}\\,dx\\,dy=\\int_0^1 y e^{y^2}\\,dy',
            'u=y^2',
            'I=\\frac12\\int_0^1e^u\\,du=\\frac{e-1}{2}',
            '\\frac{e-1}{2}',
            'D',
            'I=\\int_0^1\\int_0^y e^{y^2}\\,dx\\,dy=\\int_0^1y e^{y^2}\\,dy',
            'I=\\frac12\\int_0^1e^u\\,du=(e-1)/2',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
