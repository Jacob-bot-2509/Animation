from manim import *
FORMULAS = ['A=\\begin{pmatrix}\\cos\\theta&\\sin\\theta\\\\\\sin\\theta&-\\cos\\theta\\end{pmatrix}', 'A', 'A^TA=\\begin{pmatrix}\\cos\\theta&\\sin\\theta\\\\\\sin\\theta&-\\cos\\theta\\end{pmatrix}\\begin{pmatrix}\\cos\\theta&\\sin\\theta\\\\\\sin\\theta&-\\cos\\theta\\end{pmatrix}=\\begin{pmatrix}\\cos^2\\theta+\\sin^2\\theta&\\cos\\theta\\sin\\theta-\\sin\\theta\\cos\\theta\\\\\\sin\\theta\\cos\\theta-\\cos\\theta\\sin\\theta&\\sin^2\\theta+\\cos^2\\theta\\end{pmatrix}=I', '\\det A=-\\cos^2\\theta-\\sin^2\\theta=-1', '\\lambda^2-1=0', '\\pm 1', '1', '\\left(\\cos\\dfrac{\\theta}{2},\\sin\\dfrac{\\theta}{2}\\right)', '-1', '\\theta=(2k+1)\\pi', 'x=0', '\\tan\\dfrac{\\theta}{2}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
