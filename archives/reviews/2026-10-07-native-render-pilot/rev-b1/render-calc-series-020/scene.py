from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'f(x) = x',
            '-\\pi \\le x \\le \\pi',
            'f(x)=x',
            'a_0=a_n=0',
            'b_n=\\frac{2}{\\pi}\\int_0^\\pi x\\sin(nx)\\,dx=\\frac{2}{\\pi}[-\\frac{x\\cos(nx)}{n}+\\frac{\\sin(nx)}{n^2}]_0^\\pi=\\frac{2(-1)^{n+1}}{n}',
            'S(x)=2\\sum_{n=1}^{\\infty}\\frac{(-1)^{n+1}}{n}\\sin(nx)',
            '-\\pi<x<\\pi',
            'S(x)=x',
            'x=\\pm\\pi',
            '\\pi',
            '-\\pi',
            '0',
            '\\pm\\pi',
            'S(x)=0',
            'b_n=2(-1)^{n+1}/n',
            'S_N(x)=2\\sum_{n=1}^N(-1)^{n+1}\\sin(nx)/n',
            '\\lim_{N\\to\\infty}S_N(x)=x',
            'S_N(\\pm\\pi)=0',
            '(\\pi-\\pi)/2=0',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
