from manim import *
FORMULAS = ['\\displaystyle\\int_1^{+\\infty}\\frac{dx}{x^p}', 'p>0', 'f(x)=x^{-p}', '[1,+\\infty)', '\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{1}{n^p}', '\\displaystyle\\int_1^{+\\infty}\\dfrac{dx}{x^p}', 'p>1', 'p\\le 1', '\\int_1^b x^{-p}dx=(b^{1-p}-1)/(1-p)', 'p\\ne1', 'b^{1-p}\\to0', '1/(p-1)', 'p=1', '\\ln b\\to\\infty', '\\dfrac{1}{p-1}', '0<p\\le 1', 'y=\\dfrac{1}{x^p}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
