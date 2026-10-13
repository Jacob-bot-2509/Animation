from manim import *
FORMULAS = ['\\mathbb R[x]_{\\le4}', 'U', 'V', '(x-1)^2', 'U\\cap V', 'U+V', 'U=\\operatorname{span}(1,x^2,x^4)', '3', 'V=(x-1)^2\\mathbb R[x]_{\\le2}', 'f=a+bx^2+cx^4\\in V', 'f(1)=f^{\\prime}(1)=0', 'a+b+c=0,2b+4c=0', 'f=c(x^2-1)^2', '3+3-1=5', '\\operatorname{span}\\{(x^2-1)^2\\}', '1']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
