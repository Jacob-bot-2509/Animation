from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\mathbb{R}^2',
            '\\omega(u,v)=u_1v_2-u_2v_1',
            'J=\\begin{pmatrix}0&1\\\\-1&0\\end{pmatrix}',
            '\\omega(u,v)=u^TJv=\\det(u,v)',
            'A=\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}',
            'A^TJA=\\begin{pmatrix}0&ad-bc\\\\bc-ad&0\\end{pmatrix}=(\\det A)J',
            '\\omega(Au,Av)=(\\det A)\\omega(u,v)',
            'A',
            '\\det A=1',
            'R=\\operatorname{diag}(1,-1)',
            '-1',
            '\\omega(Ru,Rv)=-\\omega(u,v)',
            '\\omega(Au,Av)=\\omega(u,v)',
            'A^TJA=(\\det A)J',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
