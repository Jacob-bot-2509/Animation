from manim import *
FORMULAS = ['X\\sim B\\!\\left(100,\\dfrac{1}{2}\\right)', 'P(|X-50|\\ge 10)', 'E(X)=50', '\\operatorname{Var}(X)=100\\cdot\\frac12\\cdot\\frac12=25', 'q=P(|X-50|\\ge10)\\le25/10^2=1/4', 'X', '50', 'q=P(X\\le40)+P(X\\ge60)=2^{-99}\\sum_{k=0}^{40}\\binom{100}{k}', 'Y=(X-50)^2', 'Y\\ge100', 'P(X=0)>0', 'Y>100', '25=E(Y)>100q', 'q<1/4', '\\frac14', 'q=2^{-99}\\sum_{k=0}^{40}\\binom{100}{k}<\\frac14', '\\dfrac{25}{100}=\\dfrac{1}{4}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
