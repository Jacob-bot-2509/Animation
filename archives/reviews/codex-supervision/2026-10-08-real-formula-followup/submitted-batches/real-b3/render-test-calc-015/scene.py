from manim import *
FORMULAS = ['\\displaystyle\\int_0^1\\frac{\\ln(1+x)}{x}\\,dx', '\\ln(1+x)=\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{(-1)^{n-1}x^n}{n}', 'x', '\\dfrac{\\ln(1+x)}{x}=\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{(-1)^{n-1}x^{n-1}}{n}', 'x\\ne 0', '[0,1]', '\\left|\\displaystyle\\sum_{k>N}\\dfrac{(-1)^{k-1}x^{k-1}}{k}\\right|\\le\\dfrac{x^N}{N+1}\\le\\dfrac{1}{N+1}\\to 0', 'x\\in[0,1]', 'x=0', '1', '\\lim_{x\\to 0}\\dfrac{\\ln(1+x)}{x}=1', '\\displaystyle\\int_0^1\\dfrac{\\ln(1+x)}{x}dx=\\sum_{n=1}^{\\infty}\\dfrac{(-1)^{n-1}}{n}\\int_0^1x^{n-1}dx=\\sum_{n=1}^{\\infty}\\dfrac{(-1)^{n-1}}{n^2}', '\\zeta(2)', '\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{(-1)^{n-1}}{n^2}=\\eta(2)=\\left(1-2^{1-2}\\right)\\zeta(2)=\\dfrac{1}{2}\\cdot\\dfrac{\\pi^2}{6}=\\dfrac{\\pi^2}{12}', '\\zeta(2)=\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{1}{n^2}=\\dfrac{\\pi^2}{6}', '\\dfrac{\\pi^2}{12}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
