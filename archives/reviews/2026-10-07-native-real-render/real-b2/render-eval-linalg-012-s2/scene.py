from manim import *
FORMULAS = ['a', '\\begin{cases}ax+y+z=0\\\\x+ay+z=0\\\\x+y+az=0\\end{cases}', '(a-1)I+J', '(a-1)^2(a+2)', 'a\\ne1,-2', 'a=1', 'x+y+z=0', 'a=-2', '4-1=3\\ne0', '-3x+3y=0', 'z=x', '\\operatorname{span}\\{(1,1,1)^T\\}', 'x=y=z', '3-r']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
