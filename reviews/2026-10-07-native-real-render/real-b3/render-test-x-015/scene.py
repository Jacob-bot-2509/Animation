from manim import *
FORMULAS = ['P=\\begin{pmatrix}\\frac12&\\frac12\\\\\\frac14&\\frac34\\end{pmatrix}', 'P^n', 'n', 'n\\to\\infty', '\\lambda^2-\\frac54\\lambda+\\frac14=(\\lambda-1)(\\lambda-\\frac14)', '(1,1)^T', '(2,-1)^T', 'Q=\\begin{pmatrix}1&2\\\\1&-1\\end{pmatrix}', 'Q^{-1}=\\begin{pmatrix}\\frac13&\\frac23\\\\\\frac13&-\\frac13\\end{pmatrix}', 'P=Q\\operatorname{diag}(1,\\frac14)Q^{-1}', 'P^n=Q\\operatorname{diag}(1,4^{-n})Q^{-1}=\\frac13\\begin{pmatrix}1+2\\cdot4^{-n}&2-2\\cdot4^{-n}\\\\1-4^{-n}&2+4^{-n}\\end{pmatrix}', '4^{-n}\\to0', '\\lim_{n\\to\\infty}P^n=\\begin{pmatrix}\\frac13&\\frac23\\\\\\frac13&\\frac23\\end{pmatrix}', 'P^n=\\frac13\\begin{pmatrix}1+2\\cdot4^{-n}&2-2\\cdot4^{-n}\\\\1-4^{-n}&2+4^{-n}\\end{pmatrix}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
