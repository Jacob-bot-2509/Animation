from manim import *
FORMULAS = ['y=\\ln(x+\\sqrt{x^2+a^2})', 'a>0', "y'=\\dfrac{1+\\dfrac{x}{\\sqrt{x^2+a^2}}}{x+\\sqrt{x^2+a^2}}=\\dfrac{\\sqrt{x^2+a^2}+x}{\\sqrt{x^2+a^2}\\cdot(x+\\sqrt{x^2+a^2})}=\\dfrac{1}{\\sqrt{x^2+a^2}}", 'e^y=x+\\sqrt{x^2+a^2}', 'x=(e^{2y}-a^2)/(2e^y)=(e^y-a^2e^{-y})/2=a\\sinh(y-\\ln a)', '\\sqrt{x^2+a^2}=(e^y+a^2e^{-y})/2', 'x\\to\\pm\\infty', 'y\\to\\pm\\infty', '\\mathbb R', "y'=\\dfrac{1}{\\sqrt{x^2+a^2}}", 'x=a\\sinh(y-\\ln a)=\\dfrac{e^y-a^2e^{-y}}{2}', 'x+\\sqrt{x^2+a^2}', '\\sqrt{x^2+a^2}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
