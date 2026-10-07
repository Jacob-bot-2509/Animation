from manim import *
FORMULAS = ['\\displaystyle S=\\sum_{n=1}^{\\infty}\\frac{n}{2^n}', 'S=\\dfrac{1}{2}+\\dfrac{2}{4}+\\dfrac{3}{8}+\\dfrac{4}{16}+\\cdots', '\\dfrac{S}{2}=\\dfrac{1}{4}+\\dfrac{2}{8}+\\dfrac{3}{16}+\\cdots', 'S-\\dfrac{S}{2}=\\dfrac{1}{2}+\\left(\\dfrac{2}{4}-\\dfrac{1}{4}\\right)+\\left(\\dfrac{3}{8}-\\dfrac{2}{8}\\right)+\\left(\\dfrac{4}{16}-\\dfrac{3}{16}\\right)+\\cdots=\\dfrac{1}{2}+\\dfrac{1}{4}+\\dfrac{1}{8}+\\dfrac{1}{16}+\\cdots=1', '\\dfrac{S}{2}=1', 'S=2', 'a_n=n/2^n>0', 'a_{n+1}/a_n=(n+1)/(2n)\\to1/2<1', '\\sum_{n=1}^N n/2^n=2-(N+2)/2^N', '2']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
