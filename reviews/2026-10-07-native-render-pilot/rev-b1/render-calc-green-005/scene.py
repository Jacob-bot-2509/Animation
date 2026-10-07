from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\oint_L x dy - y dx',
            'L',
            'x^2 + y^2 = a^2',
            'a>0',
            'P(x,y) = -y',
            'Q(x,y) = x',
            '\\frac{\\partial Q}{\\partial x} = 1',
            '\\frac{\\partial P}{\\partial y} = -1',
            '= \\iint_D \\left( \\frac{\\partial Q}{\\partial x} - \\frac{\\partial P}{\\partial y} \\right) dxdy = \\iint_D (1 - (-1)) dxdy = 2 \\iint_D dxdy',
            '\\iint_D dxdy',
            '\\pi a^2',
            '= 2 \\pi a^2',
            '2\\pi a^2',
            'D',
            'P',
            'Q',
            '\\oint_L P dx + Q dy = \\iint_D \\left( \\frac{\\partial Q}{\\partial x} - \\frac{\\partial P}{\\partial y} \\right) dxdy',
            'a',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
