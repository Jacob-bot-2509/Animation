from manim import *
FORMULAS = ['\\displaystyle S=\\sum_{n=1}^{\\infty}\\frac{n^2}{2^n}', '\\displaystyle\\sum_{n=1}^{\\infty}x^n=\\dfrac{x}{1-x}', '\\displaystyle\\sum_{n=1}^{\\infty}nx^{n-1}=\\dfrac{1}{(1-x)^2}', '\\displaystyle\\sum_{n=1}^{\\infty}n(n-1)x^{n-2}=\\dfrac{2}{(1-x)^3}', '\\displaystyle\\sum_{n=1}^{\\infty}n^2x^n=\\sum_{n=1}^{\\infty}n(n-1)x^n+\\sum_{n=1}^{\\infty}nx^n=\\dfrac{2x^2}{(1-x)^3}+\\dfrac{x}{(1-x)^2}=\\dfrac{x(1+x)}{(1-x)^3}', 'x=\\dfrac{1}{2}', 'S=\\dfrac{(1/2)(3/2)}{(1/2)^3}=6', '6', '\\sum_{n=1}^{\\infty}n^2x^n=\\dfrac{x(1+x)}{(1-x)^3}\\quad(|x|<1)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
