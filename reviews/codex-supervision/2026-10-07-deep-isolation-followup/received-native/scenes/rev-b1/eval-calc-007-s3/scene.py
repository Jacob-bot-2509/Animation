from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'x=a\\cos^3 t',
            'y=a\\sin^3 t',
            'a>0',
            '0\\le t\\le 2\\pi',
            '\\dfrac{dy}{dx}',
            '\\dfrac{d^2y}{dx^2}',
            'F(x,y,t)=x\\sin t+y\\cos t-a\\sin t\\cos t=0',
            'F_t=0',
            'x=a\\cos^3t,\\ y=a\\sin^3t',
            '\\sin t\\cos t\\ne0',
            'F=0',
            '\\sin t+\\cos t\\,y^{\\prime}=0',
            'y^{\\prime}=-\\tan t',
            'x^{\\prime}=-3a\\cos^2t\\sin t',
            'y^{\\prime\\prime}=(-\\sec^2t)/x^{\\prime}=1/(3a\\cos^4t\\sin t)',
            'a\\cos t,a\\sin t',
            'a',
            't=k\\pi/2',
            't=k\\pi',
            't=\\pi/2+k\\pi',
            '\\dfrac{dy}{dx}=-\\tan t',
            '\\dfrac{d^2y}{dx^2}=\\dfrac{1}{3a\\cos^4 t\\sin t}',
            '\\sin t\\cos t\\ne 0',
            't=k\\dfrac{\\pi}{2}',
            'F=F_t=0',
            '\\frac{d^2y}{dx^2}',
            'y^{\\prime\\prime}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
