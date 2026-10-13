from manim import *
FORMULAS = ['X,Y', 'U(0,1)', 'P(X+Y\\le 1)', '(X,Y)', '(1-X,1-Y)', 'X+Y\\le 1\\iff (1-X)+(1-Y)\\ge 1', 'P(X+Y=1)=0', 'P(X+Y\\le 1)=P(X+Y\\ge 1)=\\dfrac{1}{2}', '\\dfrac{1}{2}', '(X,Y)\\sim(1-X,1-Y)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
