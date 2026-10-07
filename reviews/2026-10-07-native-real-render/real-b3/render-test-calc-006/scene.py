from manim import *
FORMULAS = ['f(x)=\\ln(1+x)', 'f^{(n)}(0)', "f'(x)=(1+x)^{-1}", "f''(x)=-(1+x)^{-2}", "f'''(x)=2(1+x)^{-3}", 'f^{(4)}(x)=-6(1+x)^{-4}', 'f^{(n)}(x)=(-1)^{n-1}(n-1)!\\,(1+x)^{-n}', 'n\\ge 1', 'f^{(n)}(0)=(-1)^{n-1}(n-1)!', '\\ln(1+x)=\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{(-1)^{n-1}x^n}{n}', '|x|<1', '1/(1+t)=\\sum_{k=0}^{\\infty}(-t)^k', '0', 'x', 'x=1', '1/(N+1)', '\\ln2', 'x=-1', '|x|>1', '(-1,1]', '\\ln(1+x)=\\sum_{n=1}^{\\infty}(-1)^{n-1}x^n/n', '-1<x\\le1', 'n\\ge1', '\\ln(1+x)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
