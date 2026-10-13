from manim import *
FORMULAS = ['x^{2/3}+y^{2/3}=a^{2/3}', 'a>0', "y'=-\\left(\\dfrac{y}{x}\\right)^{1/3}", "ds=\\sqrt{1+(y')^2}\\,dx=\\sqrt{1+(y/x)^{2/3}}\\,dx=\\sqrt{\\dfrac{x^{2/3}+y^{2/3}}{x^{2/3}}}\\,dx", 'ds=a^{1/3}x^{-1/3}dx', 'L_1=\\displaystyle\\int_0^a a^{1/3}x^{-1/3}dx=a^{1/3}\\left[\\dfrac{3}{2}x^{2/3}\\right]_0^a=\\dfrac{3a}{2}', 'L=4L_1=6a', 'x', '0<x\\le a', 'ds=a^{1/3}x^{-1/3}|dx|', 'x=0', 'a', 'a^{1/3}\\int_0^a x^{-1/3}dx=3a/2', '6a', "y'=-(y/x)^{1/3}", 'ds=a^{1/3}x^{-1/3}|dx|\\quad(0<x\\le a)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
