from manim import *
FORMULAS = ['\\displaystyle\\int_0^{+\\infty}e^{-x^2}\\,dx', 'I_R=\\int_0^R e^{-x^2}dx', 'I_R^2=\\iint_{[0,R]^2}e^{-(x^2+y^2)}dxdy', 'R', '\\sqrt2R', 'r', 'J_r=\\int_0^{\\pi/2}\\int_0^r e^{-u^2}u\\,du\\,d\\theta=\\frac{\\pi}{4}(1-e^{-r^2})', '\\frac{\\pi}{4}(1-e^{-R^2})\\le I_R^2\\le\\frac{\\pi}{4}(1-e^{-2R^2})', 'I_R>0', '\\pi/4', '\\int_0^\\infty e^{-x^2}dx=\\sqrt\\pi/2', '\\dfrac{\\sqrt\\pi}{2}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
