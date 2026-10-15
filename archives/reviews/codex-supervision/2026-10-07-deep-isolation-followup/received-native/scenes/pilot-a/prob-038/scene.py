from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'P(A)=\\frac{3}{5}',
            'P(B)=\\frac{2}{5}',
            'P(A\\cap B)=\\frac{1}{5}',
            'P(A\\mid B)',
            'P(B\\mid A)',
            'P(A\\mid B)=\\frac{P(A\\cap B)}{P(B)}=\\frac{1/5}{2/5}=\\frac{1}{5}\\cdot\\frac{5}{2}=\\frac{1}{2}',
            'P(B\\mid A)=\\frac{P(A\\cap B)}{P(A)}=\\frac{1/5}{3/5}=\\frac{1}{5}\\cdot\\frac{5}{3}=\\frac{1}{3}',
            'P(A\\mid B)=\\frac{1}{2}',
            'P(B\\mid A)=\\frac{1}{3}',
            '[0,1)^2',
            '2/5,1/5,1/5,1/5',
            'A\\setminus B,A\\cap B,B\\setminus A,(A\\cup B)^c',
            '1',
            'P(A)=3/5',
            'P(B)=2/5',
            'P(A\\cap B)=1/5',
            'B',
            'P(A\\mid B)=(1/5)/(2/5)=1/2',
            'A',
            'P(B\\mid A)=(1/5)/(3/5)=1/3',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
