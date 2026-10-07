from manim import *
FORMULAS = ['f(x)=x', '-\\pi<x<\\pi', '2\\pi', 'b_n=2(-1)^{n+1}/n', 'x', 'x=\\pm\\pi', '0', 'L^2', '\\sum_{n=1}^{\\infty}1/n^2', '\\dfrac{1}{\\pi}\\displaystyle\\int_{-\\pi}^{\\pi}f(x)^2dx=\\sum_{n=1}^{\\infty}b_n^2', 'a_n=0', 'b_n=\\dfrac{2(-1)^{n+1}}{n}', '\\dfrac{1}{\\pi}\\displaystyle\\int_{-\\pi}^{\\pi}x^2dx=\\dfrac{1}{\\pi}\\cdot\\dfrac{2\\pi^3}{3}=\\dfrac{2\\pi^2}{3}', '\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{4}{n^2}=4\\sum_{n=1}^{\\infty}\\dfrac{1}{n^2}', '4\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{1}{n^2}=\\dfrac{2\\pi^2}{3}', '\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{1}{n^2}=\\dfrac{\\pi^2}{6}', '\\pm\\pi', '\\dfrac{\\pi^2}{6}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
