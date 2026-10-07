from manim import *
FORMULAS = ['n', 'A', 'A^TA=I', '\\mathbb R^n', 'A^TA=I\\iff', 'x', '|Ax|^2=(Ax)^T(Ax)=x^TA^TAx=x^Tx=|x|^2', '(Ax,Ay)=\\dfrac{|A(x+y)|^2-|Ax|^2-|Ay|^2}{2}=\\dfrac{|x+y|^2-|x|^2-|y|^2}{2}=(x,y)', 'x=e_i', 'y=e_j', '(Ae_i,Ae_j)=(e_i,e_j)=\\delta_{ij}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
