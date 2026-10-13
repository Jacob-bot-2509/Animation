from manim import *
FORMULAS = ['f(x) = x', '-\\pi \\le x \\le \\pi', 'f(x)=x', 'a_0=a_n=0', 'b_n=\\frac{2}{\\pi}\\int_0^\\pi x\\sin(nx)\\,dx=\\frac{2}{\\pi}[-\\frac{x\\cos(nx)}{n}+\\frac{\\sin(nx)}{n^2}]_0^\\pi=\\frac{2(-1)^{n+1}}{n}', 'S(x)=2\\sum_{n=1}^{\\infty}\\frac{(-1)^{n+1}}{n}\\sin(nx)', '-\\pi<x<\\pi', 'S(x)=x', 'x=\\pm\\pi', '\\pi', '-\\pi', '0', '\\pm\\pi', 'S(x)=0', 'b_n=2(-1)^{n+1}/n', 'S_N(x)=2\\sum_{n=1}^N(-1)^{n+1}\\sin(nx)/n', '\\lim_{N\\to\\infty}S_N(x)=x', 'S_N(\\pm\\pi)=0', '(\\pi-\\pi)/2=0']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
