from manim import *
FORMULAS = ['y=x^2', "\\kappa(x)=\\dfrac{|y''|}{(1+y'^2)^{3/2}}=\\dfrac{2}{(1+4x^2)^{3/2}}", 'x=0', '\\kappa=2', 'R=\\dfrac{1}{2}', '\\kappa(x)', '|x|']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
