from manim import *
FORMULAS = ['A=\\begin{pmatrix} 3 & 1 \\\\ 0 & 2 \\end{pmatrix}', '|\\lambda I-A|=(\\lambda-3)(\\lambda-2)', '\\lambda=3', '(A-3I)v=0', 'v_2=0', 'E_3=\\operatorname{span}\\{(1,0)^T\\}', 't(1,0)^T', 't\\in\\mathbb R\\setminus\\{0\\}', '\\lambda=2', '(A-2I)v=0', 'v_1+v_2=0', 'E_2=\\operatorname{span}\\{(1,-1)^T\\}', 't(1,-1)^T', 'Av=3v', 'Av=2v', '3', '2', 't\\ne0']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
