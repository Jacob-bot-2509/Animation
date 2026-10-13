from manim import *
FORMULAS = ['=\\dfrac{6}{9}=\\dfrac{2}{3}', '\\dfrac{2}{3}', '\\dfrac{1}{3}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
