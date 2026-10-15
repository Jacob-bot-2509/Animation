from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'n',
            'A',
            'A^TA=I',
            '\\mathbb R^n',
            'A=(a_1,a_2,\\dots,a_n)',
            'A^TA',
            '(i,j)',
            'a_i^Ta_j=a_i\\cdot a_j',
            'A^TA=I\\iff a_i\\cdot a_j=\\delta_{ij}',
            'i,j',
            '\\iff',
            '\\sum c_ia_i=0',
            'a_j',
            'c_j=0',
            'A^TA=I\\iff',
            'a_i\\cdot a_j',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
