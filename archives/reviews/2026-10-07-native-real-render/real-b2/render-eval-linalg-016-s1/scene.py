from manim import *
FORMULAS = ['A', '\\operatorname{tr}A=5', '\\det A=6', 'A^2-5A+6I=0', '|\\lambda I-A|=\\lambda^2-(\\operatorname{tr}A)\\lambda+\\det A=\\lambda^2-5\\lambda+6=(\\lambda-2)(\\lambda-3)', '2,3', 'p(\\lambda)=\\lambda^2-5\\lambda+6', 'p(A)=A^2-5A+6I=0', '2', '3', '\\lambda^2-5\\lambda+6', '(\\lambda-2)(\\lambda-3)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
