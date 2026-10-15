from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\begin{cases}x=t^2\\\\ y=t^3-3t\\end{cases}',
            't=2',
            't',
            '\\frac{dx}{dt}=2t',
            '\\frac{dy}{dt}=3t^2-3',
            '\\frac{dy}{dx}=\\frac{3t^2-3}{2t}',
            '(4,2)',
            '\\frac{12-3}{4}=\\frac{9}{4}',
            'y-2=\\frac{9}{4}(x-4)',
            'y=\\frac{9}{4}x-7',
            '\\frac{dy}{dt}=0',
            '\\frac{dx}{dt}\\neq 0',
            '3t^2-3=0',
            't=\\pm 1',
            '(1,-2)',
            '(1,2)',
            'y=-2',
            'y=2',
            '\\frac{dx}{dt}=0',
            '\\frac{dy}{dt}\\neq 0',
            '2t=0',
            't=0',
            '\\frac{dy}{dt}=-3\\neq 0',
            '(0,0)',
            'x=0',
            '(2t,3t^2-3)',
            '2t\\ne0',
            't=\\pm1',
            '3t^2-3\\ne0',
            't,-t',
            't^3-3t=-(t^3-3t)',
            't=\\pm\\sqrt3',
            '(3,0)',
            'x=t^2,\\ y=t^3-3t',
            '\\frac{dy}{dx}=\\frac{3t^2-3}{2t}\\quad(t\\ne0)',
            't=\\pm\\sqrt{3}',
            '\\frac{9}{4}',
            'y=\\pm 2',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
