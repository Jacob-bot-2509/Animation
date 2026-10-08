from manim import *
FORMULAS = ['A_k=\\begin{pmatrix}1&k\\\\0&2\\end{pmatrix}', 'k\\in\\mathbb R', '\\alpha\\in(0,\\pi/2]', '1,2', 'e_1=(1,0)', '(k,1)', 'P=\\begin{pmatrix}1&k\\\\0&1\\end{pmatrix}', 'A_kP=P\\operatorname{diag}(1,2)', 'k', '\\cos\\alpha=|k|/\\sqrt{k^2+1}', 'k=0', 'A_k', '\\alpha=\\arccos(|k|/\\sqrt{k^2+1})']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
