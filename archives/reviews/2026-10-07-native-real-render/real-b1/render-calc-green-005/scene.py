from manim import *
FORMULAS = ['\\oint_L x dy - y dx', 'L', 'x^2 + y^2 = a^2', 'a>0', 'P(x,y) = -y', 'Q(x,y) = x', '\\frac{\\partial Q}{\\partial x} = 1', '\\frac{\\partial P}{\\partial y} = -1', '= \\iint_D \\left( \\frac{\\partial Q}{\\partial x} - \\frac{\\partial P}{\\partial y} \\right) dxdy = \\iint_D (1 - (-1)) dxdy = 2 \\iint_D dxdy', '\\iint_D dxdy', '\\pi a^2', '= 2 \\pi a^2', '2\\pi a^2', 'D', 'P', 'Q', '\\oint_L P dx + Q dy = \\iint_D \\left( \\frac{\\partial Q}{\\partial x} - \\frac{\\partial P}{\\partial y} \\right) dxdy', 'a']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
