from manim import *
FORMULAS = ['\\displaystyle\\int_1^{+\\infty}\\frac{dx}{x^p}', 'p>0', 'k\\ge0', '[2^k,2^{k+1}]', '2^{-p(k+1)}\\le x^{-p}\\le2^{-pk}', '2^{-p}2^{(1-p)k}\\le\\int_{2^k}^{2^{k+1}}x^{-p}dx\\le2^{(1-p)k}', 'p>1', '2^{1-p}<1', '0<p\\le1', '2^{-p}>0', 'x=e^t', '\\int_1^\\infty x^{-p}dx=\\int_0^\\infty e^{-(p-1)t}dt=1/(p-1)', '\\dfrac{1}{p-1}', '0<p\\le 1', '2^{-p}2^{(1-p)k}\\le A_k\\le2^{(1-p)k}', 'p=1', '1/(p-1)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
