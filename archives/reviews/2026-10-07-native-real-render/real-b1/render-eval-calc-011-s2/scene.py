from manim import *
FORMULAS = ['\\displaystyle\\sum_{n=1}^{\\infty}\\frac{1}{n\\cdot 2^n}', '\\dfrac{1}{n\\cdot 2^n}=\\displaystyle\\int_0^{1/2}x^{n-1}\\,dx', '\\dfrac{1}{2^n}', 'S=\\displaystyle\\sum_{n=1}^{\\infty}\\int_0^{1/2}x^{n-1}dx=\\int_0^{1/2}\\sum_{n=1}^{\\infty}x^{n-1}dx=\\int_0^{1/2}\\dfrac{dx}{1-x}=\\left[-\\ln(1-x)\\right]_0^{1/2}=\\ln 2', '\\ln 2', '[0,1/2]', 'x^{n-1}', '\\int_0^{1/2}x^{n-1}dx=1/(n2^n)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
