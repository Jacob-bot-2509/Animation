from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'f(x,y)=x^2-4xy+4y^2',
            'f=(x-2y)^2\\ge0',
            'x=2y',
            '(2,1)',
            '(1,-2)^T(1,-2)',
            'f=k>0',
            'x-2y=\\pm\\sqrt k',
            'k=0',
            'k>0',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
