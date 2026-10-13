from manim import *
FORMULAS = ['f(x,y)=x^2-4xy+4y^2', 'f=(x-2y)^2\\ge0', 'x=2y', '(2,1)', '(1,-2)^T(1,-2)', 'f=k>0', 'x-2y=\\pm\\sqrt k', 'k=0', 'k>0']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
