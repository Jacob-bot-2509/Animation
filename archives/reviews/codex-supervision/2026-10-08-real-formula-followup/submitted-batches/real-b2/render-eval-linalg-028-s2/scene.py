from manim import *
FORMULAS = ['\\mathbb R^2', '\\alpha=(2,3)', '\\beta_1=(1,2)', '\\beta_2=(1,1)', '\\{\\beta_1,\\beta_2\\}', 'P=\\begin{pmatrix}1&1\\\\2&1\\end{pmatrix}', '\\alpha=P\\xi', '\\xi', 'P^{-1}=\\dfrac{1}{1-2}\\begin{pmatrix}1&-1\\\\-2&1\\end{pmatrix}=\\begin{pmatrix}-1&1\\\\2&-1\\end{pmatrix}', '\\xi=P^{-1}\\alpha=\\begin{pmatrix}-1&1\\\\2&-1\\end{pmatrix}\\begin{pmatrix}2\\\\3\\end{pmatrix}=\\begin{pmatrix}-2+3\\\\4-3\\end{pmatrix}=\\begin{pmatrix}1\\\\1\\end{pmatrix}', '(1,1)', 'P^{-1}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
