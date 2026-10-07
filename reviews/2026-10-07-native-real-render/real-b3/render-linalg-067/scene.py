from manim import *
FORMULAS = ['A=\\begin{pmatrix} \\cos\\theta & -\\sin\\theta \\\\ \\sin\\theta & \\cos\\theta \\end{pmatrix}', 'A^TA=\\begin{pmatrix} \\cos\\theta & \\sin\\theta \\\\ -\\sin\\theta & \\cos\\theta \\end{pmatrix}\\begin{pmatrix} \\cos\\theta & -\\sin\\theta \\\\ \\sin\\theta & \\cos\\theta \\end{pmatrix}=I', 'A=\\begin{pmatrix}\\cos\\theta&-\\sin\\theta\\\\\\sin\\theta&\\cos\\theta\\end{pmatrix}', '\\|u-v\\|', 'A^TA=I', '\\langle Au,Av\\rangle=\\langle u,v\\rangle', '\\theta', '\\cos^2\\theta+\\sin^2\\theta=1', 'u,v', '\\|Au-Av\\|^2=(u-v)^TA^TA(u-v)=\\|u-v\\|^2', '\\det A=1']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
