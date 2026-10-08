from manim import *
FORMULAS = ['X\\sim\\operatorname{Exp}(\\lambda)', 'E[e^{tX}]', '\\lambda>0,\\ t\\in\\mathbb R', 'M(t)=E[e^{tX}]=\\displaystyle\\int_0^{\\infty}e^{tx}\\lambda e^{-\\lambda x}dx=\\lambda\\int_0^{\\infty}e^{(t-\\lambda)x}dx', 't<\\lambda', 'M(t)=\\lambda\\cdot\\dfrac{1}{\\lambda-t}=\\dfrac{\\lambda}{\\lambda-t}', 't\\ge\\lambda', 't=\\lambda', '\\int\\lambda\\,dx', 'E[e^{tX}]=\\lambda/(\\lambda-t)', '+\\infty', 't', '\\lambda']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
