from manim import *
FORMULAS = ['A=\\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}', 'A-I=\\begin{pmatrix}0&1\\\\0&0\\end{pmatrix}\\ne 0', '(A-I)^2=0', 'm(\\lambda)=(\\lambda-1)^2', '(\\lambda-1)^2', '\\iff', 'A', 'J_2(1)=\\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}', 'Av=v', '(A-I)(x,y)^T=(y,0)^T=0', 't(1,0)^T', 't\\ne0', '\\lambda=1', 't\\ne 0', '\\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}', '\\operatorname{diag}(1,1)=I']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
