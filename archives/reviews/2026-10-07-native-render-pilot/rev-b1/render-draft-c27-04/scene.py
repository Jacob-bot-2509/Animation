from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'A_k=\\begin{pmatrix}1&k\\\\0&2\\end{pmatrix}',
            'k\\in\\mathbb R',
            '\\alpha\\in(0,\\pi/2]',
            '1,2',
            'e_1=(1,0)',
            '(k,1)',
            'P=\\begin{pmatrix}1&k\\\\0&1\\end{pmatrix}',
            'A_kP=P\\operatorname{diag}(1,2)',
            'k',
            '\\cos\\alpha=|k|/\\sqrt{k^2+1}',
            'k=0',
            'A_k',
            '\\alpha=\\arccos(|k|/\\sqrt{k^2+1})',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
