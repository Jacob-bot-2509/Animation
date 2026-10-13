from manim import *
FORMULAS = ['\\vec a=(1,2,2)', '\\vec b=(-2,1,2)', '\\vec a', '\\vec b', '|\\vec a|\\cos\\theta=3\\cdot\\dfrac{4}{9}=\\dfrac{4}{3}', '\\dfrac{\\vec b}{|\\vec b|}=\\dfrac{1}{3}(-2,1,2)', '=\\dfrac{4}{3}\\cdot\\dfrac{1}{3}(-2,1,2)=\\left(-\\dfrac{8}{9},\\dfrac{4}{9},\\dfrac{8}{9}\\right)', '|\\vec a-\\vec b|^2=|(3,1,0)|^2=10', '|\\vec a|=|\\vec b|=3', '\\cos\\theta=(9+9-10)/(2\\cdot3\\cdot3)=4/9', '\\cos\\theta=\\dfrac{4}{9}', '\\left(-\\dfrac{8}{9},\\dfrac{4}{9},\\dfrac{8}{9}\\right)', '\\dfrac{4}{3}', '\\dfrac{\\vec b}{3}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
