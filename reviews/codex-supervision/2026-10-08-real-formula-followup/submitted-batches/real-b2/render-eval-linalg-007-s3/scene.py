from manim import *
FORMULAS = ['A=\\begin{pmatrix}\\cos\\theta&-\\sin\\theta\\\\\\sin\\theta&\\cos\\theta\\end{pmatrix}', 'A^n', 'n\\in\\mathbb Z_{\\ge0}', 'n=0', 'A^0=I', 'A', 'z\\mapsto e^{i\\theta}z', '(x,y)\\mapsto(x\\cos\\theta-y\\sin\\theta,\\ x\\sin\\theta+y\\cos\\theta)', 'e^{i\\theta}(x+iy)', '(e^{i\\theta})^n=e^{in\\theta}', 'A^n=', 'n\\theta', 'A^n=\\begin{pmatrix}\\cos n\\theta&-\\sin n\\theta\\\\\\sin n\\theta&\\cos n\\theta\\end{pmatrix}', 'e^{i\\theta}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
