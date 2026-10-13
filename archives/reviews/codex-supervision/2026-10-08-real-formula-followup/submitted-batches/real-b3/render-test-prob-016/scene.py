from manim import *
FORMULAS = ['P=\\begin{pmatrix}\\frac45&\\frac15\\\\\\frac25&\\frac35\\end{pmatrix}', '1', '2', '\\pi=(a,b)', 'a+b=1', 'a,b\\ge0', '\\pi P=\\pi', 'a=\\frac45a+\\frac25b', 'a=2b', 'a=\\frac23', 'b=\\frac13', '(\\frac23,\\frac13)P=(\\frac23,\\frac13)', '\\pi=(\\frac23,\\frac13)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
