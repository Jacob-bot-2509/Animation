from manim import *
FORMULAS = ['\\mathbb R^2', '\\varepsilon', '\\eta=\\{\\eta_1=(1,1),\\eta_2=(1,-1)\\}', 'P', '\\eta', '\\zeta=\\{\\zeta_1=(2,1),\\zeta_2=(1,2)\\}', 'Q', '\\zeta', 'PQ', '\\alpha', '(1,1)', 'B_\\eta=B_\\varepsilon P', 'j', '[\\eta_j]_\\varepsilon', '[v]_\\varepsilon=P[v]_\\eta', '[v]_\\eta=P^{-1}[v]_\\varepsilon', 'v', 'P=\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}', '\\zeta_1=(2,1)', '(2,1)=a(1,1)+b(1,-1)', 'a=\\frac32,b=\\frac12', '\\zeta_2=(1,2)=c(1,1)+d(1,-1)', 'c=\\frac32,d=-\\frac12', 'Q=\\begin{pmatrix}\\frac32&\\frac32\\\\\\frac12&-\\frac12\\end{pmatrix}', '\\varepsilon\\to\\zeta', 'R=PQ=\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}\\begin{pmatrix}\\frac32&\\frac32\\\\\\frac12&-\\frac12\\end{pmatrix}=\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}', '\\zeta_1,\\zeta_2', '\\alpha=1\\cdot\\zeta_1+1\\cdot\\zeta_2=(3,3)', '\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}=PQ', '(3,3)', 'PQ=\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}', '\\alpha=\\zeta_1+\\zeta_2=(3,3)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
