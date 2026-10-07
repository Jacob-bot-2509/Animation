from manim import *
FORMULAS = ['\\begin{cases}\\lambda x+y+z=1\\\\x+\\lambda y+z=\\lambda\\\\x+y+\\lambda z=\\lambda^2\\end{cases}', '\\begin{pmatrix}1&1&\\lambda&\\lambda^2\\\\0&\\lambda-1&1-\\lambda&\\lambda-\\lambda^2\\\\0&1-\\lambda&1-\\lambda^2&1-\\lambda^3\\end{pmatrix}', '\\lambda\\ne1', '\\lambda-1', '(0,1,-1,-\\lambda)', '(1-\\lambda)', '(0,0,(1-\\lambda)(\\lambda+2),(1-\\lambda)(\\lambda+1)^2)', '\\lambda\\ne1,-2', '\\lambda=-2', '0=3', '\\lambda=1', 'x+y+z=1', '\\lambda\\ne 1', '\\lambda\\ne-2']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
