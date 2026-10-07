from manim import *
FORMULAS = ['n=3', 'D=\\begin{vmatrix}a+b&a&a\\\\a&a+b&a\\\\a&a&a+b\\end{vmatrix}', 'n', 'A=bI+aJ', 'J', 'n,0,\\dots,0', 'J(1,\\dots,1)^T=n(1,\\dots,1)^T', 'A', 'b+na', 'b', 'n-1', 'D=(b+3a)\\cdot b\\cdot b=b^2(3a+b)', 'D_n=b^{n-1}(na+b)', 'b^2(3a+b)', 'b^{n-1}(na+b)', 'bI+aJ']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
