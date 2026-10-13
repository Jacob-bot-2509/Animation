from manim import *
FORMULAS = ['T\\sim\\operatorname{Exp}\\!\\left(\\dfrac{1}{1000}\\right)', '\\lambda=\\dfrac{1}{1000}', 'P(T>1500\\mid T>500)', 'P(T>t)=e^{-t/1000}', 't\\ge0', '\\{T>1500\\}\\subseteq\\{T>500\\}', 'P(T>1500\\mid T>500)=\\frac{e^{-1500/1000}}{e^{-500/1000}}=\\frac{e^{-3/2}}{e^{-1/2}}=e^{-1}', 'e^{-1}', 'S(t)=P(T>t)=e^{-t/1000}', 'P(T>500+t\\mid T>500)=S(500+t)/S(500)=S(t)', 'S(500+t)=e^{-1/2}S(t)', 'S(t)', 't=1000']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
