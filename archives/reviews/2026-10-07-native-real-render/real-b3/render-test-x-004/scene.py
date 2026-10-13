from manim import *
FORMULAS = ['P', '\\pi', '\\pi=\\pi P', 'P^T', '1', 'P=\\begin{pmatrix}\\frac12&\\frac12\\\\\\frac14&\\frac34\\end{pmatrix}', '\\pi P=\\pi', 'P^T\\pi^T=\\pi^T', '\\pi^T\\ne0', '\\pi=(a,b)', 'a+b=1', 'a=\\frac12a+\\frac14b', 'b=2a', '\\pi=(\\frac13,\\frac23)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
