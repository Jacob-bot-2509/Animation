from manim import *
FORMULAS = ['d>0', '0<l\\le d', 'X', '[0,d/2]', '\\Theta', '[0,\\pi/2]', 'x\\sim U\\!\\left(0,\\dfrac{d}{2}\\right)', '\\theta\\sim U\\!\\left(0,\\dfrac{\\pi}{2}\\right)', 'x\\le\\dfrac{l}{2}\\sin\\theta', 'f(x,\\theta)=\\dfrac{2}{d}\\cdot\\dfrac{2}{\\pi}', 'P=\\dfrac{4}{\\pi d}\\displaystyle\\int_0^{\\pi/2}\\!\\!\\int_0^{(l/2)\\sin\\theta}dx\\,d\\theta=\\dfrac{4}{\\pi d}\\int_0^{\\pi/2}\\dfrac{l}{2}\\sin\\theta\\,d\\theta=\\dfrac{2l}{\\pi d}\\left[-\\cos\\theta\\right]_0^{\\pi/2}=\\dfrac{2l}{\\pi d}', '\\dfrac{2l}{\\pi d}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
