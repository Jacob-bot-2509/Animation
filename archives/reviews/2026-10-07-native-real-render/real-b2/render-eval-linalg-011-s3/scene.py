from manim import *
FORMULAS = ['\\begin{cases}\\lambda x+y+z=1\\\\x+\\lambda y+z=\\lambda\\\\x+y+\\lambda z=\\lambda^2\\end{cases}', '\\lambda=1', 'x+y+z=1', '\\lambda=-2', '(\\lambda-1)I+J', '(\\lambda-1)^2(\\lambda+2)', '\\lambda\\ne1,-2', '1-2+4=3', '(1,1,1)', '\\lambda\\ne 1', '\\lambda\\ne-2', '\\lambda']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
