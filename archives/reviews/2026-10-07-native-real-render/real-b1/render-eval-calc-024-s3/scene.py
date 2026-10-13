from manim import *
FORMULAS = ['\\arctan x', '\\dfrac{\\pi}{4}=1-\\dfrac{1}{3}+\\dfrac{1}{5}-\\dfrac{1}{7}+\\cdots', 'f(x)=\\arctan x', 'f^{(n)}(0)', "f'(x)=\\dfrac{1}{1+x^2}", '\\arctan', '|f^{(m)}(t)|\\le(m-1)!', 'm\\ge 1', 't', '|R_N(x)|=\\dfrac{|f^{(N+1)}(\\xi)|}{(N+1)!}|x|^{N+1}\\le\\dfrac{N!}{(N+1)!}\\cdot 1=\\dfrac{1}{N+1}\\to 0', '|x|\\le 1', 'm\\ge1', 'f^{(m)}(t)=\\frac{(-1)^{m-1}(m-1)!}{2i}[(t-i)^{-m}-(t+i)^{-m}]', '|f^{(m)}(t)|\\le(m-1)!(1+t^2)^{-m/2}\\le(m-1)!', 'f^{(2k+1)}(0)=(-1)^k(2k)!', 'f^{(2k)}(0)=0', '1/(N+1)', '\\arctan x=\\displaystyle\\sum_{n=0}^{\\infty}\\dfrac{(-1)^n x^{2n+1}}{2n+1}', 'x=1', '\\dfrac{1}{N+1}\\to0']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
