from manim import *
FORMULAS = ['2x^2+y^2-z^2+4xy=1', 'z=0', '2x^2+4xy+y^2=1', '2(x+y)^2-y^2=1', 'y=0', '2x^2-z^2=1', 'x+y=0', 'x=-y', '-y^2-z^2=1', 'z', 'x+y', 'u=x+y,\\ v=y,\\ w=z', '2u^2-v^2-w^2=1', 'u=\\pm\\sqrt{(1+v^2+w^2)/2}', '\\mathbb R^2', '|u|\\ge1/\\sqrt2']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
