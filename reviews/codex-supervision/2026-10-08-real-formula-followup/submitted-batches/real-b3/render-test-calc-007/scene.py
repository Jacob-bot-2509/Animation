from manim import *
FORMULAS = ['f', "f(0)=f'(0)=0", '\\displaystyle\\lim_{x\\to 0}\\frac{f(x)}{x^2}', 'f(0)=0', "f'(0)=0", '\\dfrac{f(x)}{x^2}', '\\dfrac{0}{0}', "\\lim_{x\\to 0}\\dfrac{f'(x)}{2x}", "f''", "\\lim_{x\\to 0}\\dfrac{f'(x)}{2x}=\\dfrac{1}{2}\\lim_{x\\to 0}\\dfrac{f'(x)-f'(0)}{x}=\\dfrac{f''(0)}{2}", "\\dfrac{f''(0)}{2}"]
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
