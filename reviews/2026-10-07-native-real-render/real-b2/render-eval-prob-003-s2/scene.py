from manim import *
FORMULAS = ['E', '\\dfrac{1}{2}', '1+E', 'E=\\dfrac{1}{2}\\cdot 1+\\dfrac{1}{2}\\cdot(1+E)=1+\\dfrac{E}{2}', 'E=2', 'X', 'P(X>2k)=4^{-k}', 'E[X]\\le2\\sum_{k=0}^{\\infty}4^{-k}=8/3<\\infty', 'E[X]=2', '2', 'E=1+\\dfrac{E}{2}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
