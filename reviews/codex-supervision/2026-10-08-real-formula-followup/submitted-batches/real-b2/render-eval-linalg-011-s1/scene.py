from manim import *
FORMULAS = ['\\begin{cases}\\lambda x+y+z=1\\\\x+\\lambda y+z=\\lambda\\\\x+y+\\lambda z=\\lambda^2\\end{cases}', 'D=\\begin{vmatrix}\\lambda&1&1\\\\1&\\lambda&1\\\\1&1&\\lambda\\end{vmatrix}', '=(\\lambda-1)I+J', 'J', '(\\lambda-1)+3=\\lambda+2', '\\lambda-1', 'D=(\\lambda+2)(\\lambda-1)^2', '\\lambda\\ne 1,-2', 'D\\ne 0', '\\lambda=1', 'x+y+z=1', '\\lambda=-2', '0\\cdot(x+y+z)=1+(-2)+4=3', '0=3', '\\lambda\\ne 1', '\\lambda\\ne-2']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
