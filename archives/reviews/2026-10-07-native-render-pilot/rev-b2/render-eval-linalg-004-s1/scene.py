from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'n=3',
            'D=\\begin{vmatrix}a+b&a&a\\\\a&a+b&a\\\\a&a&a+b\\end{vmatrix}',
            'n',
            'D=\\begin{vmatrix}a+b&a&a\\\\-b&b&0\\\\-b&0&b\\end{vmatrix}',
            'D=(a+b)\\cdot b^2-a\\cdot\\begin{vmatrix}-b&0\\\\-b&b\\end{vmatrix}+a\\cdot\\begin{vmatrix}-b&b\\\\-b&0\\end{vmatrix}=(a+b)b^2-a(-b^2)+a(b^2)=b^2(a+b)+ab^2+ab^2=b^2(3a+b)',
            'n\\ge2',
            'M=bI+aJ',
            'R_i\\leftarrow R_i-R_1',
            'i=2,\\ldots,n',
            'i',
            '-b',
            'b',
            'C_1\\leftarrow C_1+C_2+\\cdots+C_n',
            '(na+b,0,\\ldots,0)^T',
            '\\det M=(na+b)b^{n-1}',
            'n=1',
            'a+b',
            'b=0',
            'b^2(3a+b)',
            'b^{n-1}(na+b)',
            '2\\le i\\le n',
            'C_1\\leftarrow\\sum_{j=1}^nC_j',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
