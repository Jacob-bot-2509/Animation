from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'F_1=F_2=1',
            'F_{n+2}=F_{n+1}+F_n',
            'F_{10}',
            'F_0=0',
            '\\binom{F_{n+1}}{F_n}=A^n\\binom10',
            'A=\\begin{pmatrix}1&1\\\\1&0\\end{pmatrix}',
            '\\phi=(1+\\sqrt5)/2',
            '\\psi=(1-\\sqrt5)/2',
            'Q=\\begin{pmatrix}\\phi&\\psi\\\\1&1\\end{pmatrix}',
            'A=Q\\operatorname{diag}(\\phi,\\psi)Q^{-1}',
            '\\det Q=\\sqrt5\\ne0',
            'F_n=(\\phi^n-\\psi^n)/\\sqrt5',
            'F_{10}=55',
            'r=\\psi/\\phi',
            '|r|<1',
            'n\\ge1',
            '\\frac{F_{n+1}}{F_n}=\\phi\\frac{1-r^{n+1}}{1-r^n}\\to\\phi=\\frac{1+\\sqrt5}{2}',
            '\\lim_{n\\to\\infty}\\frac{F_{n+1}}{F_n}=\\frac{1+\\sqrt5}{2}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
