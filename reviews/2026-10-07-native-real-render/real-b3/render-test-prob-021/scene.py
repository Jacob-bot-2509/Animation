from manim import *
FORMULAS = ['A,B', 'P(A)=\\frac25', 'P(A\\cup B)=\\frac7{10}', 'P(B)', 'p=P(B)', 'P(A\\cap B)=\\frac25p', '\\frac7{10}=\\frac25+p-\\frac25p=\\frac25+\\frac35p', '\\frac35p=\\frac3{10}', 'p=\\frac12', '\\frac12']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
