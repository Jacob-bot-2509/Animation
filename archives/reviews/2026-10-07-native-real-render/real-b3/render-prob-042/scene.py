from manim import *
FORMULAS = ['X_1,X_2,\\ldots', 'P(X_i=1)=p', 'P(X_i=0)=1-p', '0\\le p\\le1', 'F_n=n^{-1}\\sum_{i=1}^nX_i', 'E(F_n)', '\\operatorname{Var}(F_n)', 'F_n\\xrightarrow{P}p', 'p', 'X_i\\sim\\operatorname{Bernoulli}(p)', 'p=P(X_i=1)', 'p=\\frac{1}{2}', 'F_n=\\frac{1}{n}\\sum_{i=1}^n X_i', 'E(F_n)=p', '\\operatorname{Var}(F_n)=p(1-p)/n', '\\varepsilon>0', 'P(|F_n-p|\\ge\\varepsilon)\\le\\frac{p(1-p)}{n\\varepsilon^2}\\to0', '\\operatorname{Var}(F_n)=\\frac{p(1-p)}n', 'p=\\frac12', '(p)', 'y=p', 'P(|F_n-p|\\ge\\varepsilon)\\le\\min\\{1,p(1-p)/(n\\varepsilon^2)\\}\\to0', 'p=1/2']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
