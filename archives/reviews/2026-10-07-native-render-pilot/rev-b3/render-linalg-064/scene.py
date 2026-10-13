from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'A=\\begin{pmatrix} 3 & 1 \\\\ 0 & 2 \\end{pmatrix}',
            '|\\lambda I-A|=(\\lambda-3)(\\lambda-2)',
            '\\lambda=3',
            '(A-3I)v=0',
            'v_2=0',
            'E_3=\\operatorname{span}\\{(1,0)^T\\}',
            't(1,0)^T',
            't\\in\\mathbb R\\setminus\\{0\\}',
            '\\lambda=2',
            '(A-2I)v=0',
            'v_1+v_2=0',
            'E_2=\\operatorname{span}\\{(1,-1)^T\\}',
            't(1,-1)^T',
            'Av=3v',
            'Av=2v',
            '3',
            '2',
            't\\ne0',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
