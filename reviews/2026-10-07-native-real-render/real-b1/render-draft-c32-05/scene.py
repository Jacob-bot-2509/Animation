from manim import *
FORMULAS = ['Ax=0', '\\mathbb R^n', 'n-\\mathrm{rank}(A)', 'Ax=b', 'b\\neq0', '\\eta_0+\\ker A', '\\ker A', 'n-\\operatorname{rank}A', 'x_0', 'A(x-x_0)=0', 'x_0+\\ker A', 'b\\ne0', 'b=0']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
