from manim import *
FORMULAS = ['\\alpha_1=(1,2,3)', '\\alpha_2=(2,3,1)', '\\alpha_3=(3,1,2)', '|D|=18\\ne 0', '\\alpha_2\\times\\alpha_3=(5,-1,-7)', '\\alpha_1\\cdot(\\alpha_2\\times\\alpha_3)=5-2-21=-18']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
