from manim import *
FORMULAS = ['\\displaystyle\\sum_{n=1}^{\\infty}\\frac{(-1)^{n-1}}{n}=\\ln 2', '\\ln(1+x)=\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{(-1)^{n-1}x^n}{n}', '|x|<1', 'x=1', '\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{(-1)^{n-1}}{n}', 'a_n=\\dfrac{1}{n}\\searrow 0', '\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{(-1)^{n-1}}{n}=\\lim_{x\\to 1^-}\\ln(1+x)=\\ln 2', '\\dfrac{1}{n}=\\displaystyle\\int_0^1x^{n-1}dx', '\\displaystyle\\sum_{n=1}^{N}\\dfrac{(-1)^{n-1}}{n}=\\int_0^1\\sum_{n=1}^{N}(-x)^{n-1}dx=\\int_0^1\\dfrac{1-(-x)^N}{1+x}dx\\to\\int_0^1\\dfrac{dx}{1+x}=\\ln 2', '\\left|\\int_0^1\\frac{(-x)^N}{1+x}dx\\right|\\le\\int_0^1x^Ndx=1/(N+1)\\to0', '\\ln 2', 'x\\to 1^-']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
