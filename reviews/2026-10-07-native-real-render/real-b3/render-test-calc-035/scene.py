from manim import *
FORMULAS = ['\\displaystyle\\sum_{n=0}^{\\infty}\\frac{x^n}{n!}', '\\displaystyle\\sum_{n=0}^{\\infty}n!\\,x^n', '\\sum_{n=0}^{\\infty}x^n/n!', 'x\\ne0', '|x|/(n+1)\\to0', 'x', '+\\infty', '\\sum_{n=0}^{\\infty}n!x^n', '(n+1)|x|\\to\\infty', 'x=0', 'R=+\\infty', 'R=0', '1/n!', 'n!']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
