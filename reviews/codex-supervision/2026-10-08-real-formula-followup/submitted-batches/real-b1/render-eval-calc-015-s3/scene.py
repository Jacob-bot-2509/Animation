from manim import *
FORMULAS = ['\\displaystyle I=\\int_0^\\pi\\frac{x\\sin x}{1+\\cos^2 x}\\,dx', 'g(x)=\\sin x/(1+\\cos^2x)', '0\\le x\\le\\pi', 'g(\\pi-x)=g(x)', 'x=\\pi-t', 'I=\\int_0^\\pi(\\pi-t)g(t)\\,dt', '2I=\\pi\\int_0^\\pi g(x)\\,dx', 'u=\\cos x', '\\int_0^\\pi g(x)\\,dx=\\int_{-1}^1(1+u^2)^{-1}\\,du=\\arctan1-\\arctan(-1)=\\pi/2', 'I=\\pi^2/4', '\\frac{\\pi^2}{4}', '\\int_0^\\pi g(x)\\,dx=\\int_{-1}^1(1+u^2)^{-1}\\,du=\\pi/2']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
