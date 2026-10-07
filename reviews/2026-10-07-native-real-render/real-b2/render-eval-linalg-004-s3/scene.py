from manim import *
FORMULAS = ['n=3', 'D=\\begin{vmatrix}a+b&a&a\\\\a&a+b&a\\\\a&a&a+b\\end{vmatrix}', 'n', '(a,a,a)^T+b\\,e_i', 'e_i', 'b\\,e_i', 'b^3\\det I=b^3', '(a,a,a)^T', 'ab^2\\cdot\\det(e_1,e_2,e_j', '(1,1,1)^T)=ab^2', 'D=b^3+3ab^2=b^2(3a+b)', 'n\\ge2', 'be_j+a\\mathbf1', 'a\\mathbf1', 'be_j', 'b^n', 'ab^{n-1}', '\\mathbf1=\\sum_j e_j', 'e_j', 'b^n+nab^{n-1}=(na+b)b^{n-1}', 'n=1', 'a+b', 'b^2(3a+b)', 'b^{n-1}(na+b)', 'b', 'a']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
