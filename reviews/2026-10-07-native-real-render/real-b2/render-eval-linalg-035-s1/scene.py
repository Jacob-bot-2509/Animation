from manim import *
FORMULAS = ['n', 'A', 'A^TA=I', '\\mathbb R^n', 'A=(a_1,a_2,\\dots,a_n)', 'A^TA', '(i,j)', 'a_i^Ta_j=a_i\\cdot a_j', 'A^TA=I\\iff a_i\\cdot a_j=\\delta_{ij}', 'i,j', '\\iff', '\\sum c_ia_i=0', 'a_j', 'c_j=0', 'A^TA=I\\iff', 'a_i\\cdot a_j']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
