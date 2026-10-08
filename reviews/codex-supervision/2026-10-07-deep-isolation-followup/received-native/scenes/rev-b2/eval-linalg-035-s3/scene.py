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
            'e_1,\\ldots,e_n',
            'a_i=Ae_i',
            'a_i\\cdot a_j=e_i^TA^TAe_j=\\delta_{ij}',
            '\\sum_i c_i a_i=0',
            'a_j',
            'c_j=0',
            '(A^TA)_{ij}=a_i\\cdot a_j=\\delta_{ij}',
            '\\pm1',
            '\\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}',
            'A^TA=I\\iff',
            'a_i\\cdot a_j=e_i^TA^TAe_j',
            'a_i\\cdot a_j=\\delta_{ij}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
