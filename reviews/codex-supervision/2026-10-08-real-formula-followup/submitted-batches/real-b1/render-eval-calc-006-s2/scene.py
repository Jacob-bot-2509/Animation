from manim import *
FORMULAS = ['y=\\ln(x+\\sqrt{x^2+a^2})', 'a>0', 'x=a\\sinh t', 'x+\\sqrt{x^2+a^2}=a(\\sinh t+\\cosh t)=a e^t', 'y=\\ln(ae^t)=t+\\ln a', 'y=\\operatorname{arsinh}\\dfrac{x}{a}+\\ln a', "(\\operatorname{arsinh} u)'=\\dfrac{u'}{\\sqrt{1+u^2}}", "y'=\\dfrac{1/a}{\\sqrt{1+x^2/a^2}}=\\dfrac{1}{\\sqrt{x^2+a^2}}", 'e^y=x+\\sqrt{x^2+a^2}', 'x=(e^{2y}-a^2)/(2e^y)=(e^y-a^2e^{-y})/2=a\\sinh(y-\\ln a)', '\\sqrt{x^2+a^2}=(e^y+a^2e^{-y})/2', 'x\\to\\pm\\infty', 'y\\to\\pm\\infty', '\\mathbb R', "y'=\\dfrac{1}{\\sqrt{x^2+a^2}}", 'x=a\\sinh(y-\\ln a)=\\dfrac{e^y-a^2e^{-y}}{2}', 'Y^2-X^2=a^2', 'X=a\\sinh t,\\ Y=a\\cosh t', '\\sinh t+\\cosh t=e^t', 'x=a\\sinh(y-\\ln a)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
