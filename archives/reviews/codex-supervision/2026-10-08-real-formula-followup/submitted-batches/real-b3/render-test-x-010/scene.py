from manim import *
FORMULAS = ['\\sigma_1,\\sigma_2>0', '\\begin{pmatrix}\\sigma_1^2&\\rho\\sigma_1\\sigma_2\\\\\\rho\\sigma_1\\sigma_2&\\sigma_2^2\\end{pmatrix}', '|\\rho|<1', '\\sigma_1^2>0', '\\sigma_1^2\\sigma_2^2(1-\\rho^2)', '\\iff', '\\iff 1-\\rho^2>0\\iff|\\rho|<1', 'X-E[X]', 'Y-E[Y]', 'a,b', 'aX+bY', '\\iff|\\rho|<1', '\\rho=\\pm 1']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
