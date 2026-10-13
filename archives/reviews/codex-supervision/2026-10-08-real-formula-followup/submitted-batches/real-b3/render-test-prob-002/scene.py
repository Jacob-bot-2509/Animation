from manim import *
FORMULAS = ['X\\sim B\\!\\left(10,\\dfrac{3}{10}\\right)', 'P(X=3)', 'P(X\\le 1)', 'P(X=3)=\\binom{10}{3}\\left(\\frac3{10}\\right)^3\\left(\\frac7{10}\\right)^7=\\frac{120\\cdot3^3\\cdot7^7}{10^{10}}=\\frac{66706983}{250000000}', 'P(X\\le1)=P(X=0)+P(X=1)=\\left(\\frac7{10}\\right)^{10}+10\\cdot\\frac3{10}\\left(\\frac7{10}\\right)^9=\\frac{7^{10}+30\\cdot7^9}{10^{10}}=\\frac{1493083459}{10000000000}', 'P(X=3)=\\frac{66706983}{250000000}', 'P(X\\le1)=\\frac{1493083459}{10000000000}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
