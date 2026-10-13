from manim import *
FORMULAS = ['\\frac35', '\\frac25', '\\frac1{50}', '\\frac3{100}', 'A_i', 'i', 'D', 'P(A_1\\cap D)=\\frac35\\cdot\\frac1{50}=\\frac3{250}', 'P(A_2\\cap D)=\\frac25\\cdot\\frac3{100}=\\frac3{250}', 'P(D)=\\frac3{125}>0', 'P(A_1\\mid D)=\\frac{3/250}{3/125}=\\frac12', '\\frac12']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
