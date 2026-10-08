from manim import *
FORMULAS = ['\\vec a,\\vec b', '|\\vec a\\cdot\\vec b|\\le|\\vec a||\\vec b|', '\\vec b=\\vec 0', '\\vec b\\ne\\vec 0', '\\vec a', '\\vec a=\\vec a_\\parallel+\\vec a_\\perp', '\\vec a_\\parallel=\\dfrac{\\vec a\\cdot\\vec b}{|\\vec b|^2}\\vec b', '\\vec b', '\\vec a_\\perp\\perp\\vec b', '|\\vec a|^2=|\\vec a_\\parallel|^2+|\\vec a_\\perp|^2\\ge|\\vec a_\\parallel|^2=\\dfrac{(\\vec a\\cdot\\vec b)^2}{|\\vec b|^2}', '\\vec a_\\perp=\\vec 0', '|\\vec a|^2\\ge|\\vec a_\\parallel|^2']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
