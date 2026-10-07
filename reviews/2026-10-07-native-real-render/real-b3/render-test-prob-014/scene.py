from manim import *
FORMULAS = ['E', '\\dfrac{1}{6}', '\\dfrac{5}{6}', '1+E', 'E=\\dfrac{1}{6}\\cdot 1+\\dfrac{5}{6}\\cdot(1+E)=1+\\dfrac{5E}{6}', 'E=6', 'p=\\dfrac{1}{6}', '\\dfrac{1}{p}=6', 'P(T>k)=(5/6)^k', 'E[T]=\\sum_{k=0}^\\infty P(T>k)=\\sum_{k=0}^\\infty(5/6)^k=6<\\infty', '6']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
