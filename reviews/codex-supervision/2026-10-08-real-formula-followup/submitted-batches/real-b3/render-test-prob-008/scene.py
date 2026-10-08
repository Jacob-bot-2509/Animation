from manim import *
FORMULAS = ['n', '\\bar X_n', 'P(|\\bar X_n-\\frac72|\\ge\\frac1{10})', 'n\\to\\infty', '0', 'X_i', '1,\\ldots,6', 'E(X_i)=\\frac16\\sum_{k=1}^6k=\\frac72', 'E(X_i^2)=\\frac16\\sum_{k=1}^6k^2=\\frac{91}{6}', '\\operatorname{Var}(X_i)=\\frac{91}{6}-\\frac{49}{4}=\\frac{35}{12}', 'E(\\bar X_n)=\\frac72', '\\operatorname{Var}(\\bar X_n)=\\frac{35}{12n}', 'P(|\\bar X_n-\\frac72|\\ge\\frac1{10})\\le\\min\\{1,\\frac{35}{12n}\\cdot100\\}=\\min\\{1,\\frac{875}{3n}\\}', '\\min\\{1,\\frac{875}{3n}\\}', 'E(X_i)=7/2', '\\operatorname{Var}(X_i)=35/12', '\\operatorname{Var}(\\overline X_n)=35/(12n)', '1/10', 'P(|\\overline X_n-7/2|\\ge1/10)\\le\\min\\{1,875/(3n)\\}\\to0']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
