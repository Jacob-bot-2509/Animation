from manim import *
FORMULAS = ['A=\\begin{pmatrix}1&2\\\\2&1\\end{pmatrix}', 'q_1=\\dfrac{1}{\\sqrt2}(1,1)^T', 'q_2=\\dfrac{1}{\\sqrt2}(1,-1)^T', 'Q=\\dfrac{1}{\\sqrt2}\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}', 'Q', 'Q^{-1}=Q^T', 'Q^TAQ=\\begin{pmatrix}3&0\\\\0&-1\\end{pmatrix}', 'Q^TAQ=\\dfrac{1}{2}\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}\\begin{pmatrix}1&2\\\\2&1\\end{pmatrix}\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}=\\dfrac{1}{2}\\begin{pmatrix}3&3\\\\-1&1\\end{pmatrix}\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}=\\dfrac{1}{2}\\begin{pmatrix}6&0\\\\0&-2\\end{pmatrix}', '\\lambda_1=3', '\\lambda_2=-1', '(1,1)^T', '(1,-1)^T', 'P^{-1}AP=\\begin{pmatrix}3&0\\\\0&-1\\end{pmatrix}', 'P=\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}', '\\det Q=-1', 'Q^TAQ=\\operatorname{diag}(3,-1)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
