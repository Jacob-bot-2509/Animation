from manim import *
FORMULAS = ['n', 'A', 'A^TA=I', '\\mathbb R^n', 'e_1,\\ldots,e_n', 'a_i=Ae_i', 'a_i\\cdot a_j=e_i^TA^TAe_j=\\delta_{ij}', '\\sum_i c_i a_i=0', 'a_j', 'c_j=0', '(A^TA)_{ij}=a_i\\cdot a_j=\\delta_{ij}', '\\pm1', '\\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}', 'A^TA=I\\iff', 'a_i\\cdot a_j=e_i^TA^TAe_j', 'a_i\\cdot a_j=\\delta_{ij}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
