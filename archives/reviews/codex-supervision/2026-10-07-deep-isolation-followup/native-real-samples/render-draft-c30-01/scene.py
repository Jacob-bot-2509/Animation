from manim import *
FORMULAS = ['5', 'x=1', 'x=2', 'f(0)=1', '(x-1)^3\\mid f', '(x-2)^2\\mid f', '(x-1)^3(x-2)^2\\mid f', '\\deg f\\le5', 'f=c(x-1)^3(x-2)^2', 'c\\in\\mathbb R', '-4c=1', 'c=-\\frac14', 'c(x-2)^2', '-\\frac14\\ne0', '3', 'c(x-1)^3', '2', 'c', 'f(x)=-\\frac14(x-1)^3(x-2)^2', 'x=1,2', '3,2', '-4c=1\\Rightarrow c=-\\frac14']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
