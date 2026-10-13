from manim import *
FORMULAS = ['X\\sim B\\!\\left(100,\\dfrac{1}{2}\\right)', 'P(|X-50|\\ge 10)', '\\binom{100}{k}=\\binom{100}{100-k}', 'q=P(X\\le40)+P(X\\ge60)=\\frac{2}{2^{100}}\\sum_{k=0}^{40}\\binom{100}{k}', 'E(X)=50', '\\operatorname{Var}(X)=25', '1/4', 'S=\\sum_{k=0}^{40}\\binom{100}{k}', '\\frac14-q=\\frac{2^{97}-S}{2^{99}}', 'E((X-50)^2)>100P(|X-50|\\ge10)', 'X=0', '\\frac14', '\\frac{1}{2^{99}}\\sum_{k=0}^{40}\\binom{100}{k}', '|X-50|<10', 'P(X\\ge60)=P(X\\le40)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
