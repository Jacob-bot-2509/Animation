from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'f(x)=x^5+x+1',
            'f(x)',
            'x-1',
            'x^2+1',
            'ax+b',
            'f(x)=(x^2+1)q(x)+ax+b',
            'x=i',
            'x=-i',
            'f(i)=1+2i',
            'f(-i)=(-i)^5-i+1=-i-i+1=1-2i',
            '\\begin{cases}ai+b=1+2i\\\\-ai+b=1-2i\\end{cases}',
            '2b=2',
            'b=1',
            '2ai=4i',
            'a=2',
            '2x+1',
            'f(1)=1+1+1=3',
            '3',
            'x=\\pm i',
            'ai+b=1+2i',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
