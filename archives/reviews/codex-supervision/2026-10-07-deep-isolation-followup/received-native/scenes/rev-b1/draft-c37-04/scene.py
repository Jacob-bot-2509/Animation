from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\mathbb R^2',
            '\\varepsilon',
            '\\eta=\\{\\eta_1=(1,1),\\eta_2=(1,-1)\\}',
            'P',
            '\\eta',
            '\\zeta=\\{\\zeta_1=(2,1),\\zeta_2=(1,2)\\}',
            'Q',
            '\\zeta',
            'PQ',
            '\\alpha',
            '(1,1)',
            'B_\\eta=B_\\varepsilon P',
            'j',
            '[\\eta_j]_\\varepsilon',
            '[v]_\\varepsilon=P[v]_\\eta',
            '[v]_\\eta=P^{-1}[v]_\\varepsilon',
            'v',
            'P=\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}',
            '\\zeta_1=(2,1)',
            '(2,1)=a(1,1)+b(1,-1)',
            'a=\\frac32,b=\\frac12',
            '\\zeta_2=(1,2)=c(1,1)+d(1,-1)',
            'c=\\frac32,d=-\\frac12',
            'Q=\\begin{pmatrix}\\frac32&\\frac32\\\\\\frac12&-\\frac12\\end{pmatrix}',
            '\\varepsilon\\to\\zeta',
            'R=PQ=\\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}\\begin{pmatrix}\\frac32&\\frac32\\\\\\frac12&-\\frac12\\end{pmatrix}=\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}',
            '\\zeta_1,\\zeta_2',
            '\\alpha=1\\cdot\\zeta_1+1\\cdot\\zeta_2=(3,3)',
            '\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}=PQ',
            '(3,3)',
            'PQ=\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}',
            '\\alpha=\\zeta_1+\\zeta_2=(3,3)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
