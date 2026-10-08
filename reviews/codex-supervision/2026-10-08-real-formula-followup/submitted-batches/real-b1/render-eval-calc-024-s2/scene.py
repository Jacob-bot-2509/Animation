from manim import *
FORMULAS = ['\\arctan x', '\\dfrac{\\pi}{4}=1-\\dfrac{1}{3}+\\dfrac{1}{5}-\\dfrac{1}{7}+\\cdots', 'x=1', '\\displaystyle\\sum_{n=0}^{\\infty}\\dfrac{(-1)^n}{2n+1}', 'a_n=\\dfrac{1}{2n+1}\\searrow 0', '\\arctan 1=\\dfrac{\\pi}{4}=1-\\dfrac{1}{3}+\\dfrac{1}{5}-\\dfrac{1}{7}+\\cdots', 'x=-1', '1/(1+t^2)=\\sum_{k=0}^{\\infty}(-1)^kt^{2k}', '[-r,r]', 'r<1', '0', '\\arctan x=\\displaystyle\\sum_{n=0}^{\\infty}\\dfrac{(-1)^n x^{2n+1}}{2n+1}', '|x|\\le 1', '\\dfrac{\\pi}{4}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
