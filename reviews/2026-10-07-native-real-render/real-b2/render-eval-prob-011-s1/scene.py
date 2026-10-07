from manim import *
FORMULAS = ['E_0', 'E_1', 'E_0=1+\\dfrac{1}{2}E_0+\\dfrac{1}{2}E_1', 'E_1=1+\\dfrac{1}{2}\\cdot 0+\\dfrac{1}{2}E_0', 'E_1=1+\\dfrac{E_0}{2}', 'E_0=1+\\dfrac{E_0}{2}+\\dfrac{1}{2}\\left(1+\\dfrac{E_0}{2}\\right)=\\dfrac{3}{2}+\\dfrac{3E_0}{4}', 'E_0=6', '1/4', 'T', 'P(T>2k)\\le(3/4)^k', 'E[T]\\le2\\sum_{k=0}^{\\infty}(3/4)^k=8<\\infty', '6', 'E_0=1+\\dfrac12E_0+\\dfrac12E_1']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
