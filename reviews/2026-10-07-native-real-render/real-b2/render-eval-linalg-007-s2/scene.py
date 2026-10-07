from manim import *
FORMULAS = ['A=\\begin{pmatrix}\\cos\\theta&-\\sin\\theta\\\\\\sin\\theta&\\cos\\theta\\end{pmatrix}', 'A^n', 'n\\in\\mathbb Z_{\\ge0}', 'n=0', 'A^0=I', '(\\cos\\theta-\\lambda)^2+\\sin^2\\theta=0', '\\lambda^2-2\\lambda\\cos\\theta+1=0', '\\lambda=e^{\\pm i\\theta}', '(1,\\mp i)^T', 'P=\\begin{pmatrix}1&1\\\\-i&i\\end{pmatrix}', 'P^{-1}=\\dfrac{1}{2}\\begin{pmatrix}1&i\\\\1&-i\\end{pmatrix}', 'A=P\\begin{pmatrix}e^{i\\theta}&0\\\\0&e^{-i\\theta}\\end{pmatrix}P^{-1}', 'A^n=P\\begin{pmatrix}e^{in\\theta}&0\\\\0&e^{-in\\theta}\\end{pmatrix}P^{-1}=\\dfrac{1}{2}\\begin{pmatrix}e^{in\\theta}+e^{-in\\theta}&i(e^{in\\theta}-e^{-in\\theta})\\\\-i(e^{in\\theta}-e^{-in\\theta})&e^{in\\theta}+e^{-in\\theta}\\end{pmatrix}=\\begin{pmatrix}\\cos n\\theta&-\\sin n\\theta\\\\\\sin n\\theta&\\cos n\\theta\\end{pmatrix}', 'e^{\\pm in\\theta}=\\cos n\\theta\\pm i\\sin n\\theta', 'A^n=\\begin{pmatrix}\\cos n\\theta&-\\sin n\\theta\\\\\\sin n\\theta&\\cos n\\theta\\end{pmatrix}', 'e^{\\pm i\\theta}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
