from manim import *
FORMULAS = ['A', '365^{30}', '365\\cdot364\\cdots336=365!/335!', 'P(A^c)=\\frac{365!}{335!\\,365^{30}}', 'P(A)=1-\\frac{365!}{335!\\,365^{30}}', '1-\\frac{365!}{335!\\,365^{30}}', '\\dfrac{365\\cdot364\\cdots336}{365^{30}}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
