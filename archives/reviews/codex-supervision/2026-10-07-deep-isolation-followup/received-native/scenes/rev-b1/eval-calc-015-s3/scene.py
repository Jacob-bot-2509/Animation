from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\displaystyle I=\\int_0^\\pi\\frac{x\\sin x}{1+\\cos^2 x}\\,dx',
            'g(x)=\\sin x/(1+\\cos^2x)',
            '0\\le x\\le\\pi',
            'g(\\pi-x)=g(x)',
            'x=\\pi-t',
            'I=\\int_0^\\pi(\\pi-t)g(t)\\,dt',
            '2I=\\pi\\int_0^\\pi g(x)\\,dx',
            'u=\\cos x',
            '\\int_0^\\pi g(x)\\,dx=\\int_{-1}^1(1+u^2)^{-1}\\,du=\\arctan1-\\arctan(-1)=\\pi/2',
            'I=\\pi^2/4',
            '\\frac{\\pi^2}{4}',
            '\\int_0^\\pi g(x)\\,dx=\\int_{-1}^1(1+u^2)^{-1}\\,du=\\pi/2',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
