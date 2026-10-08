from manim import *
FORMULAS = ['\\displaystyle I=\\int_0^1\\!\\!\\int_x^1 e^{y^2}\\,dy\\,dx', 'D=\\{(x,y):0\\le x\\le y\\le1\\}', 'I=\\int_0^1\\int_0^y e^{y^2}\\,dx\\,dy=\\int_0^1 y e^{y^2}\\,dy', 'u=y^2', 'I=\\frac12\\int_0^1e^u\\,du=\\frac{e-1}{2}', '\\frac{e-1}{2}', 'D', 'I=\\int_0^1\\int_0^y e^{y^2}\\,dx\\,dy=\\int_0^1y e^{y^2}\\,dy', 'I=\\frac12\\int_0^1e^u\\,du=(e-1)/2']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
