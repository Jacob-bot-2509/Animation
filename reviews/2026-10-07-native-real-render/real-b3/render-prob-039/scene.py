from manim import *
FORMULAS = ['Q=[-1,1]^2', 'n\\ge1', 'D=\\{(x,y):x^2+y^2\\le1\\}', 'm_n', '\\widehat\\pi_n=4m_n/n', '\\widehat\\pi_n\\xrightarrow{P}\\pi', '4m_n/n', '\\pi', 'Q', 'I_i', 'i', 'D', 'm_n=\\sum_{i=1}^n I_i', 'P(I_i=1)=\\frac{\\pi}{4}', '\\widehat\\pi_n=\\frac{4m_n}{n}', 'E(\\widehat\\pi_n)=\\pi', '\\operatorname{Var}(\\widehat\\pi_n)=\\frac{\\pi(4-\\pi)}{n}', '\\varepsilon>0', 'P(|\\widehat\\pi_n-\\pi|\\ge\\varepsilon)\\le\\frac{\\pi(4-\\pi)}{n\\varepsilon^2}\\to0', '[-1,1]^2', 'p=\\pi/4', '\\operatorname{Var}(\\widehat\\pi_n)=\\pi(4-\\pi)/n', 'P(|\\widehat\\pi_n-\\pi|\\ge\\varepsilon)\\le\\pi(4-\\pi)/(n\\varepsilon^2)\\to0']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
