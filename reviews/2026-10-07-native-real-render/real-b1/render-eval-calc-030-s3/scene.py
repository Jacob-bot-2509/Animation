from manim import *
FORMULAS = ['y=\\sin x', '0\\le x\\le\\pi', 'x', 'y', '0\\le y\\le 1', 'x=\\arcsin y', 'x=\\pi-\\arcsin y', 'R=\\pi-\\arcsin y', 'r=\\arcsin y', 'V=\\pi\\displaystyle\\int_0^1\\left[(\\pi-\\arcsin y)^2-(\\arcsin y)^2\\right]dy=\\pi\\int_0^1(\\pi^2-2\\pi\\arcsin y)\\,dy=\\pi\\left[\\pi^2y-2\\pi\\int_0^1\\arcsin y\\,dy\\right]', '\\displaystyle\\int_0^1\\arcsin y\\,dy=\\left[y\\arcsin y+\\sqrt{1-y^2}\\right]_0^1=\\dfrac{\\pi}{2}-1', 'V=\\pi\\left[\\pi^2-2\\pi\\left(\\dfrac{\\pi}{2}-1\\right)\\right]=\\pi\\left[\\pi^2-\\pi^2+2\\pi\\right]=2\\pi^2', '2\\pi^2', '\\pi-\\arcsin y', '\\arcsin y']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
