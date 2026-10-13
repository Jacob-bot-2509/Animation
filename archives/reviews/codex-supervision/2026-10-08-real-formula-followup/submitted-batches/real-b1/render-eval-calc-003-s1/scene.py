from manim import *
FORMULAS = ['\\displaystyle\\lim_{n\\to\\infty}\\left(1+\\frac{1}{n}\\right)^n', 'e', '\\displaystyle\\sum_{k=0}^{\\infty}\\frac{1}{k!}', 'a_n=\\left(1+\\dfrac{1}{n}\\right)^n', 'a_n=\\sum_{k=0}^{n}\\binom{n}{k}\\dfrac{1}{n^k}=\\sum_{k=0}^{n}\\dfrac{1}{k!}\\cdot\\dfrac{n(n-1)\\cdots(n-k+1)}{n^k}', 'a_n', 'a_{n+1}', 'k', '\\dfrac{n(n-1)\\cdots(n-k+1)}{n^k}\\le\\dfrac{(n+1)n\\cdots(n-k+2)}{(n+1)^k}', 'a_{n+1}>a_n', 'a_n\\le\\sum_{k=0}^{n}\\dfrac{1}{k!}\\le 1+1+\\dfrac{1}{2}+\\dfrac{1}{4}+\\cdots+\\dfrac{1}{2^{n-1}}<3', '\\lim a_n', 'E=\\sum_{k=0}^{\\infty}1/k!', 'k!\\ge2^{k-1}', 'k\\ge1', 'a_n=\\sum_{k=0}^{n}c_{k,n}/k!', 'c_{0,n}=c_{1,n}=1', 'c_{k,n}=\\prod_{j=0}^{k-1}(1-j/n)\\in[0,1]', 'm', 'n\\ge m', '\\sum_{k=0}^{m}c_{k,n}/k!\\le a_n\\le E', 'n\\to\\infty', 'm\\to\\infty', '\\lim a_n=E', 'e=\\sum_{k=0}^{\\infty}\\frac{1}{k!}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
