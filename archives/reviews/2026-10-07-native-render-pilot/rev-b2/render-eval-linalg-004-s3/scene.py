from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'n=3',
            'D=\\begin{vmatrix}a+b&a&a\\\\a&a+b&a\\\\a&a&a+b\\end{vmatrix}',
            'n',
            '(a,a,a)^T+b\\,e_i',
            'e_i',
            'b\\,e_i',
            'b^3\\det I=b^3',
            '(a,a,a)^T',
            'ab^2\\cdot\\det(e_1,e_2,e_j',
            '(1,1,1)^T)=ab^2',
            'D=b^3+3ab^2=b^2(3a+b)',
            'n\\ge2',
            'be_j+a\\mathbf1',
            'a\\mathbf1',
            'be_j',
            'b^n',
            'ab^{n-1}',
            '\\mathbf1=\\sum_j e_j',
            'e_j',
            'b^n+nab^{n-1}=(na+b)b^{n-1}',
            'n=1',
            'a+b',
            'b^2(3a+b)',
            'b^{n-1}(na+b)',
            'b',
            'a',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
