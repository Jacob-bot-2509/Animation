from manim import *
FORMULAS = ['\\pi_1:x+y+z=1', '\\pi_2:x+2y+3z=6', '(x,y,z)=(-4+t,5-2t,t)', '\\pi_1', '(-4+t)+(5-2t)+t=1', '\\pi_2', '(-4+t)+2(5-2t)+3t=-4+t+10-4t+3t=6', 'z=t', 'y+2t=5', 'y=5-2t', 'x=t-4', '\\dfrac{x+4}{1}=\\dfrac{y-5}{-2}=\\dfrac{z}{1}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
