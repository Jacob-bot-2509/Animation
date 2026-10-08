from manim import *
FORMULAS = ['A=\\begin{pmatrix}0&1\\\\0&0\\end{pmatrix}', 'e^{tA}', 't', '(sI-A)^{-1}=\\begin{pmatrix}s&-1\\\\0&s\\end{pmatrix}^{-1}=\\dfrac{1}{s^2}\\begin{pmatrix}s&1\\\\0&s\\end{pmatrix}=\\begin{pmatrix}1/s&1/s^2\\\\0&1/s\\end{pmatrix}', '\\mathcal L^{-1}\\{1/s\\}=1', '\\mathcal L^{-1}\\{1/s^2\\}=t', 'e^{tA}=\\begin{pmatrix}1&t\\\\0&1\\end{pmatrix}', 't\\ge0', '\\Phi(t)=I+tA', '\\Phi^{\\prime}=A\\Phi', '\\Phi(0)=I', '\\Phi(t)=e^{tA}', '(sI-A)^{-1}=\\begin{pmatrix}1/s&1/s^2\\\\0&1/s\\end{pmatrix}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
