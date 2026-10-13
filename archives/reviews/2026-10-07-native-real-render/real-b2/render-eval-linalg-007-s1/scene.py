from manim import *
FORMULAS = ['A=\\begin{pmatrix}\\cos\\theta&-\\sin\\theta\\\\\\sin\\theta&\\cos\\theta\\end{pmatrix}', 'A^n', 'n\\in\\mathbb Z_{\\ge0}', 'n=0', 'A^0=I', 'n=1', 'A^k=\\begin{pmatrix}\\cos k\\theta&-\\sin k\\theta\\\\\\sin k\\theta&\\cos k\\theta\\end{pmatrix}', 'A^{k+1}=A^kA', '(1,1)', '\\cos k\\theta\\cos\\theta-\\sin k\\theta\\sin\\theta=\\cos(k+1)\\theta', '(1,2)', '-\\cos k\\theta\\sin\\theta-\\sin k\\theta\\cos\\theta=-\\sin(k+1)\\theta', 'A^n=\\begin{pmatrix}\\cos n\\theta&-\\sin n\\theta\\\\\\sin n\\theta&\\cos n\\theta\\end{pmatrix}', 'n\\theta']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
