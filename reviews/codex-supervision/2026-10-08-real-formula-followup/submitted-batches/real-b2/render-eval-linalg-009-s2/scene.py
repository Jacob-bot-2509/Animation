from manim import *
FORMULAS = ['M=\\begin{pmatrix}2&1&1\\\\1&2&1\\\\0&0&3\\end{pmatrix}', '\\det M=(-1)^{3+3}\\cdot 3\\cdot\\begin{vmatrix}2&1\\\\1&2\\end{vmatrix}=3\\cdot 3=9', '2\\times2', 'B=\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}', 'C=(3)', '\\det M=\\det B\\det C=3\\cdot3=9', '9', '(-1)^{3+3}\\cdot3']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
