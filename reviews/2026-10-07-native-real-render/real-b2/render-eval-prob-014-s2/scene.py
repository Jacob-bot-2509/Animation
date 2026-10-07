from manim import *
FORMULAS = ['X\\sim\\operatorname{Exp}(\\lambda)', '\\lambda>0', 'P(X>s+t\\mid X>s)=P(X>t)', 's,t>0', 'h(t)=\\dfrac{f(t)}{1-F(t)}=\\dfrac{\\lambda e^{-\\lambda t}}{e^{-\\lambda t}}=\\lambda', '\\lambda', "\\dfrac{F'}{1-F}=\\lambda", 'F(t)=1-e^{-\\lambda t}', 'F(0)=0', 'S=1-F', 'S^{\\prime}=-\\lambda S', 'S(0)=1', 'S(t)=e^{-\\lambda t}', 'P(X>s+t\\mid X>s)=S(s+t)/S(s)=e^{-\\lambda t}=P(X>t)', 'h(t)=\\lambda']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
