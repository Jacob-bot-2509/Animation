from manim import *
FORMULAS = ['x^8-1', 'x^8-1=(x^4-1)(x^4+1)=(x^2-1)(x^2+1)(x^4+1)=(x-1)(x+1)(x^2+1)(x^4+1)', 'x^4+1', 'x^4+1=(x^2-\\sqrt2x+1)(x^2+\\sqrt2x+1)', '(x-1)(x+1)(x^2+1)(x^2-\\sqrt2x+1)(x^2+\\sqrt2x+1)', 'e^{2\\pi ik/8}', 'k=0,\\ldots,7', 'x^8-1=\\prod_{k=0}^7(x-e^{2\\pi ik/8})', '-4,-2,-2', '\\displaystyle\\prod_{k=0}^{7}\\left(x-e^{2\\pi ik/8}\\right)', '(x^4-1)(x^4+1)\\to\\cdots']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
