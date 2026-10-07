from manim import *
FORMULAS = ['X,Y', '\\operatorname{Geom}\\!\\left(\\dfrac{1}{2}\\right)', 'P(X=k)=P(Y=k)=\\left(\\dfrac{1}{2}\\right)^k', 'P(X=Y)=\\displaystyle\\sum_{k=1}^{\\infty}P(X=k)P(Y=k)=\\sum_{k=1}^{\\infty}\\left(\\dfrac{1}{2}\\right)^{2k}=\\sum_{k=1}^{\\infty}\\left(\\dfrac{1}{4}\\right)^k=\\dfrac{1/4}{1-1/4}=\\dfrac{1}{3}', '\\dfrac{1}{3}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
