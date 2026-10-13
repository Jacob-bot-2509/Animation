from manim import *
FORMULAS = ['F_1=F_2=1', 'F_{n+2}=F_{n+1}+F_n', 'F_{10}', 'F_0=0', '\\binom{F_{n+1}}{F_n}=A^n\\binom10', 'A=\\begin{pmatrix}1&1\\\\1&0\\end{pmatrix}', '\\phi=(1+\\sqrt5)/2', '\\psi=(1-\\sqrt5)/2', 'Q=\\begin{pmatrix}\\phi&\\psi\\\\1&1\\end{pmatrix}', 'A=Q\\operatorname{diag}(\\phi,\\psi)Q^{-1}', '\\det Q=\\sqrt5\\ne0', 'F_n=(\\phi^n-\\psi^n)/\\sqrt5', 'F_{10}=55', 'r=\\psi/\\phi', '|r|<1', 'n\\ge1', '\\frac{F_{n+1}}{F_n}=\\phi\\frac{1-r^{n+1}}{1-r^n}\\to\\phi=\\frac{1+\\sqrt5}{2}', '\\lim_{n\\to\\infty}\\frac{F_{n+1}}{F_n}=\\frac{1+\\sqrt5}{2}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
