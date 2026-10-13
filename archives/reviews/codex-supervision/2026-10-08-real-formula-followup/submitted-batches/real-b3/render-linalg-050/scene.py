from manim import *
FORMULAS = ['\\begin{vmatrix} a & b \\\\ c & d \\end{vmatrix} = ad - bc', 'A=\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}', 'u=(a,c)^T', 'v=(b,d)^T', '0,u,u+v,v', '\\det(u,v)=ad-bc', '|ad-bc|', '\\det A>0', '\\det A<0', '\\det A=0', '\\operatorname{rank}A\\le1', '1', '0', 'A=0', 'ad-bc', '\\operatorname{rank}A=1', '\\operatorname{rank}A=0']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
