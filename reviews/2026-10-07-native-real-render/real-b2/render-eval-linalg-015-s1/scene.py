from manim import *
FORMULAS = ['A=\\begin{pmatrix}1&2\\\\2&1\\end{pmatrix}', '|\\lambda I-A|=\\begin{vmatrix}\\lambda-1&-2\\\\-2&\\lambda-1\\end{vmatrix}=(\\lambda-1)^2-4=\\lambda^2-2\\lambda-3=(\\lambda-3)(\\lambda+1)', '\\lambda=3,-1', '\\lambda=3', '(3I-A)v=0', '\\begin{pmatrix}2&-2\\\\-2&2\\end{pmatrix}v=0', 'v=(1,1)^T', '\\lambda=-1', '(-I-A)v=0', '\\begin{pmatrix}-2&-2\\\\-2&-2\\end{pmatrix}v=0', 'v=(1,-1)^T', 'P=((1,1)^T,(1,-1)^T)=\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}', '\\det P=-2\\ne0', 'AP=P\\operatorname{diag}(3,-1)', 'P^{-1}AP=\\operatorname{diag}(3,-1)', '\\lambda_1=3', '\\lambda_2=-1', '(1,1)^T', '(1,-1)^T', 'P^{-1}AP=\\begin{pmatrix}3&0\\\\0&-1\\end{pmatrix}', 'P=\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}', '(\\lambda-3)(\\lambda+1)=0']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
