from manim import *
FORMULAS = ['\\displaystyle S=\\sum_{n=1}^{\\infty}\\frac{n^2}{2^n}', 'A=\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{n}{2^n}=2', 'B=\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{1}{2^n}=1', '\\dfrac{S}{2}=\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{n^2}{2^{n+1}}=\\sum_{m=2}^{\\infty}\\dfrac{(m-1)^2}{2^m}', 'S-\\dfrac{S}{2}=\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{n^2-(n-1)^2}{2^n}=\\sum_{n=1}^{\\infty}\\dfrac{2n-1}{2^n}=2A-B=2\\cdot 2-1=3', '\\dfrac{S}{2}=3', 'S=6', 'a_{n+1}/a_n=(n+1)^2/(2n^2)\\to1/2<1', '\\sum_{n=1}^N n^2/2^n=6-(N^2+4N+6)/2^N', '6', 'A=2', 'B=1']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
