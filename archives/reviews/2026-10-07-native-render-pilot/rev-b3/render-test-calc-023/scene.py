from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'f(x)=x',
            '-\\pi<x<\\pi',
            '2\\pi',
            'b_n=2(-1)^{n+1}/n',
            'x',
            'x=\\pm\\pi',
            '0',
            'L^2',
            '\\sum_{n=1}^{\\infty}1/n^2',
            '\\dfrac{1}{\\pi}\\displaystyle\\int_{-\\pi}^{\\pi}f(x)^2dx=\\sum_{n=1}^{\\infty}b_n^2',
            'a_n=0',
            'b_n=\\dfrac{2(-1)^{n+1}}{n}',
            '\\dfrac{1}{\\pi}\\displaystyle\\int_{-\\pi}^{\\pi}x^2dx=\\dfrac{1}{\\pi}\\cdot\\dfrac{2\\pi^3}{3}=\\dfrac{2\\pi^2}{3}',
            '\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{4}{n^2}=4\\sum_{n=1}^{\\infty}\\dfrac{1}{n^2}',
            '4\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{1}{n^2}=\\dfrac{2\\pi^2}{3}',
            '\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{1}{n^2}=\\dfrac{\\pi^2}{6}',
            '\\pm\\pi',
            '\\dfrac{\\pi^2}{6}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
