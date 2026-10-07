from manim import *
FORMULAS = ['\\mathbb R^2', '\\operatorname{span}\\{(1,1)^T\\}', '(3,1)^T', '\\hat u=\\dfrac{1}{\\sqrt2}(1,1)^T', 'P=\\hat u\\hat u^T=\\dfrac{1}{2}\\begin{pmatrix}1&1\\\\1&1\\end{pmatrix}=\\begin{pmatrix}\\frac{1}{2}&\\frac{1}{2}\\\\\\frac{1}{2}&\\frac{1}{2}\\end{pmatrix}', 'P\\begin{pmatrix}3\\\\1\\end{pmatrix}=\\begin{pmatrix}\\frac{1}{2}&\\frac{1}{2}\\\\\\frac{1}{2}&\\frac{1}{2}\\end{pmatrix}\\begin{pmatrix}3\\\\1\\end{pmatrix}=\\begin{pmatrix}2\\\\2\\end{pmatrix}', 'P^2=P', '(3,1)^T-(2,2)^T=(1,-1)^T\\perp(1,1)^T', 'P=\\begin{pmatrix}\\frac{1}{2}&\\frac{1}{2}\\\\\\frac{1}{2}&\\frac{1}{2}\\end{pmatrix}', '(2,2)^T', 'y=x']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
