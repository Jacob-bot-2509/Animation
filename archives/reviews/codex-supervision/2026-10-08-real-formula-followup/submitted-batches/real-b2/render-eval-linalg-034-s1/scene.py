from manim import *
FORMULAS = ['\\vec a,\\vec b', '|\\vec a\\cdot\\vec b|\\le|\\vec a||\\vec b|', '\\vec b=\\vec 0', '\\vec b\\ne\\vec 0', 't', '0\\le|\\vec a+t\\vec b|^2=|\\vec a|^2+2t(\\vec a\\cdot\\vec b)+t^2|\\vec b|^2', '\\Delta=4(\\vec a\\cdot\\vec b)^2-4|\\vec a|^2|\\vec b|^2\\le 0', '(\\vec a\\cdot\\vec b)^2\\le|\\vec a|^2|\\vec b|^2', '\\vec a+t\\vec b=\\vec 0', '\\vec a', '\\vec b', '\\Delta\\le0']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
