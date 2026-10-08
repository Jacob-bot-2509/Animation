from manim import *
FORMULAS = ['a\\in\\mathbb R', '\\lambda', 'A(\\lambda)=\\begin{pmatrix}\\lambda-a&1&0\\\\0&\\lambda-1&1\\\\0&0&\\lambda-1\\end{pmatrix}', 'A(\\lambda)', 'a', 'B(a)=\\begin{pmatrix}a&-1&0\\\\0&1&-1\\\\0&0&1\\end{pmatrix}', 'A(\\lambda)=\\lambda I-B(a)', 'e_3=(0,0,1)^T', '(e_3,\\ B e_3,\\ B^2 e_3)=\\begin{pmatrix}0&0&1\\\\0&-1&-2\\\\1&1&1\\end{pmatrix},\\qquad \\det=1\\neq 0,', '\\{e_3,Be_3,B^2e_3\\}', 'e_3', 'B', 'm_B', '\\chi_B(\\lambda)=(\\lambda-a)(\\lambda-1)^2', 'm_B=\\chi_B', '1,\\ 1,\\ (\\lambda-a)(\\lambda-1)^2', 'a\\neq 1', '\\lambda-a', '(\\lambda-1)^2', '\\operatorname{diag}\\!\\bigl(a,\\,J_2(1)\\bigr)', 'J_2(1)=\\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}', 'a=1', '(\\lambda-1)^3', 'J_3(1)=\\begin{pmatrix}1&1&0\\\\0&1&1\\\\0&0&1\\end{pmatrix}', 'J_2(1)', '\\neq 1', 'J_1(a)\\oplus J_2(1)', 'J_3(1)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
