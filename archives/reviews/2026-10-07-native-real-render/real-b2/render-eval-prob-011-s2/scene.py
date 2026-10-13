from manim import *
FORMULAS = ['\\{0,1,H\\}', 'H', 'P=\\begin{pmatrix}1/2&1/2&0\\\\1/2&0&1/2\\\\0&0&1\\end{pmatrix}', 'Q=\\begin{pmatrix}1/2&1/2\\\\1/2&0\\end{pmatrix}', 'N=(I-Q)^{-1}=\\begin{pmatrix}1/2&-1/2\\\\-1/2&1\\end{pmatrix}^{-1}=4\\begin{pmatrix}1&1/2\\\\1/2&1/2\\end{pmatrix}=\\begin{pmatrix}4&2\\\\2&2\\end{pmatrix}', '\\det(I-Q)=\\dfrac{1}{2}-\\dfrac{1}{4}=\\dfrac{1}{4}', 'N', '=4+2=6', '1/4', 'T', 'P(T>2k)\\le(3/4)^k', 'E[T]\\le2\\sum_{k=0}^{\\infty}(3/4)^k=8<\\infty', '6', 'N=(I-Q)^{-1}=\\begin{pmatrix}4&2\\\\2&2\\end{pmatrix}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
