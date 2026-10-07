from manim import *
FORMULAS = ['A=\\begin{pmatrix}1&2\\\\2&1\\end{pmatrix}', 'u=(x+y)/\\sqrt2,\\ v=(x-y)/\\sqrt2', 'x=(u+v)/\\sqrt2,\\ y=(u-v)/\\sqrt2', 'x^2+y^2=u^2+v^2', '4xy=2u^2-2v^2', 'f=3u^2-v^2', 'Q=\\frac1{\\sqrt2}\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}', 'Q^TAQ=\\operatorname{diag}(3,-1)', '3,-1', 'P=\\sqrt2Q', 'P^{-1}AP=\\operatorname{diag}(3,-1)', '\\lambda_1=3', '\\lambda_2=-1', '(1,1)^T', '(1,-1)^T', 'P^{-1}AP=\\begin{pmatrix}3&0\\\\0&-1\\end{pmatrix}', 'P=\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}', 'x^2+4xy+y^2']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
