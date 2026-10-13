from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'A,B',
            'P(A)=\\frac25',
            'P(A\\cup B)=\\frac7{10}',
            'P(B)',
            'p=P(B)',
            'P(A\\cap B)=\\frac25p',
            '\\frac7{10}=\\frac25+p-\\frac25p=\\frac25+\\frac35p',
            '\\frac35p=\\frac3{10}',
            'p=\\frac12',
            '\\frac12',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
