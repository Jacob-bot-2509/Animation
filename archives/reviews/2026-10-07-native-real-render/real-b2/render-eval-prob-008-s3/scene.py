from manim import *
FORMULAS = ['X\\sim B\\!\\left(100,\\dfrac{1}{2}\\right)', 'P(|X-50|\\ge 10)', 'A=\\{|X-50|\\ge10\\}', 'E((X-50)^2)=25', 'P(A)\\le1/4', 'q=2^{-99}\\sum_{k=0}^{40}\\binom{100}{k}', '25-100q=E(((X-50)^2-100)\\mathbf1_A)+E((X-50)^2\\mathbf1_{A^c})>0', 'X=0', 'q<1/4', '\\frac14-q=\\frac{2^{97}-\\sum_{k=0}^{40}\\binom{100}{k}}{2^{99}}>0', '\\frac14', 'E(X)=50', '\\operatorname{Var}(X)=25', 'P(|X-50|\\ge10)\\le1/4', '1/4-q=(2^{97}-\\sum_{k=0}^{40}\\binom{100}{k})/2^{99}>0', '100']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
