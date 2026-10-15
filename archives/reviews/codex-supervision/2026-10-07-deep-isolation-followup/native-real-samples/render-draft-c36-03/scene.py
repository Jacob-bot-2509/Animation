from manim import *
FORMULAS = ['A=\\operatorname{diag}(1,-1,0)', 'C=\\begin{pmatrix}1&1&0\\\\0&2&0\\\\0&0&3\\end{pmatrix}', 'B=C^{\\mathsf T}AC', 'B', '(n_+,n_-,n_0)', 'A', '\\det C=6\\ne0', 'B=\\begin{pmatrix}1&1&0\\\\1&-3&0\\\\0&0&0\\end{pmatrix}', 'v', 'v^{\\mathsf T}Bv=(Cv)^{\\mathsf T}A(Cv)', 'v\\mapsto Cv', '\\operatorname{rank}B=\\operatorname{rank}A=2', '3-2=1', '(1,1,1)', 'S', 'B=S^{-1}AS', '\\operatorname{tr}(UV)=\\operatorname{tr}(VU)', '\\operatorname{tr}B=\\operatorname{tr}A', '\\operatorname{tr}A=0', '\\operatorname{tr}B=-2', '\\operatorname{rank}B=2', '(n_+,n_-,n_0)=(1,1,1)', 'A,B', '0,-2', 'A,C,B=C^{\\mathsf T}AC', '\\det C=6', '2', '\\det C\\ne0']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
