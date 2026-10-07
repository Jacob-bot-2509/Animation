from manim import *
FORMULAS = ['e^x=2x+1', 'f(x)=e^x-2x-1', "f'(x)=e^x-2", 'f', '(-\\infty,\\ln2)', '(\\ln2,+\\infty)', 'f(0)=0', '\\ln2=\\int_1^2t^{-1}\\,dt>1/2', 'f(\\ln2)=1-2\\ln2<0', 'e^2>1+2+2=5', 'f(2)>0', '0<\\ln2<1', '0', '\\xi', '(\\ln2,2)', '\\xi\\in(\\ln2,2)', 'y=e^x', 'y=2x+1']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
