from manim import *
FORMULAS = ['20', 'h(t)=20-5t^2', 't', "v(t)=h'(t)=-10t", "a(t)=v'(t)=-10", 'h(t)=0', '20-5t^2=0', 't=2', 'v(2)=-20', 'v(t)=-10t', 'a(t)=-10', '^2', '-20']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
