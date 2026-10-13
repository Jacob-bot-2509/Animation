from manim import *
FORMULAS = ['X\\sim\\operatorname{Exp}(1)', 'E[X^n]=n!', 'n\\in\\mathbb Z_{\\ge0}', 'n\\in\\{0,1,2,\\dots\\}', 'E[X^n]=\\displaystyle\\int_0^{\\infty}x^ne^{-x}dx', 'I_n=\\displaystyle\\int_0^{\\infty}x^ne^{-x}dx', 'I_0=\\displaystyle\\int_0^{\\infty}e^{-x}dx=1', 'n\\ge 1', 'u=x^n', 'dv=e^{-x}dx', 'I_n=\\left[-x^ne^{-x}\\right]_0^{\\infty}+n\\displaystyle\\int_0^{\\infty}x^{n-1}e^{-x}dx=nI_{n-1}', 'x^ne^{-x}\\big|_0^\\infty', 'I_n=n!', '\\Gamma(n+1)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
