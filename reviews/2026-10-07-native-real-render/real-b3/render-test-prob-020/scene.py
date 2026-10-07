from manim import *
FORMULAS = ['10', '1', 'K', '1,\\ldots,10', 'P(K=k)=1/10', 'E(K)=\\frac1{10}\\sum_{k=1}^{10}k=\\frac{10\\cdot11}{2\\cdot10}=\\frac{11}{2}', '\\frac{11}{2}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
