from manim import *
FORMULAS = ['\\displaystyle\\lim_{n\\to\\infty}\\left(1+\\frac{1}{n}\\right)^n', 'e', '\\displaystyle\\sum_{k=0}^{\\infty}\\frac{1}{k!}', 'n\\ln\\left(1+\\dfrac{1}{n}\\right)=\\dfrac{\\ln(1+x)}{x}', 'x=\\dfrac{1}{n}\\to 0^+', '\\lim_{x\\to 0^+}\\dfrac{\\ln(1+x)}{x}=\\lim_{x\\to 0^+}\\dfrac{1}{1+x}=1', '\\lim n\\ln(1+1/n)=1', '=e^1', 'E(x)=\\sum_{k=0}^{\\infty}x^k/k!', 'E^{\\prime}=E', 'E(0)=1', '(e^{-x}E(x))^{\\prime}=0', 'E(x)=e^x', 'e=\\sum_{k=0}^{\\infty}1/k!', 'e=\\sum_{k=0}^{\\infty}\\frac{1}{k!}', 'y=\\dfrac{\\ln(1+x)}{x}', 'x\\to0^+']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
