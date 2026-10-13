from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'y=\\sin x',
            '0\\le x\\le\\pi',
            'x',
            'y',
            '0\\le y\\le 1',
            'x=\\arcsin y',
            'x=\\pi-\\arcsin y',
            'R=\\pi-\\arcsin y',
            'r=\\arcsin y',
            'V=\\pi\\displaystyle\\int_0^1\\left[(\\pi-\\arcsin y)^2-(\\arcsin y)^2\\right]dy=\\pi\\int_0^1(\\pi^2-2\\pi\\arcsin y)\\,dy=\\pi\\left[\\pi^2y-2\\pi\\int_0^1\\arcsin y\\,dy\\right]',
            '\\displaystyle\\int_0^1\\arcsin y\\,dy=\\left[y\\arcsin y+\\sqrt{1-y^2}\\right]_0^1=\\dfrac{\\pi}{2}-1',
            'V=\\pi\\left[\\pi^2-2\\pi\\left(\\dfrac{\\pi}{2}-1\\right)\\right]=\\pi\\left[\\pi^2-\\pi^2+2\\pi\\right]=2\\pi^2',
            '2\\pi^2',
            '\\pi-\\arcsin y',
            '\\arcsin y',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
