from manim import *
FORMULAS = ['\\displaystyle\\int_1^{+\\infty}\\frac{dx}{x^p}', 'p>0', 'p\\ne 1', '\\displaystyle\\int_1^b x^{-p}dx=\\left[\\dfrac{x^{1-p}}{1-p}\\right]_1^b=\\dfrac{b^{1-p}-1}{1-p}', 'p>1', '1-p<0', 'b^{1-p}\\to 0', '\\dfrac{0-1}{1-p}=\\dfrac{1}{p-1}', '0<p<1', 'b^{1-p}\\to+\\infty', 'p=1', '\\displaystyle\\int_1^b\\dfrac{dx}{x}=\\ln b\\to+\\infty', '\\dfrac{1}{p-1}', '0<p\\le 1', 'p\\ne1', '(b^{1-p}-1)/(1-p)', '\\ln b', '1/(p-1)', '0<p\\le1']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
