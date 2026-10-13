from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'A',
            '\\operatorname{tr}A=5',
            '\\det A=6',
            'A^2-5A+6I=0',
            '|\\lambda I-A|=\\lambda^2-(\\operatorname{tr}A)\\lambda+\\det A=\\lambda^2-5\\lambda+6=(\\lambda-2)(\\lambda-3)',
            '2,3',
            'p(\\lambda)=\\lambda^2-5\\lambda+6',
            'p(A)=A^2-5A+6I=0',
            '2',
            '3',
            '\\lambda^2-5\\lambda+6',
            '(\\lambda-2)(\\lambda-3)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
