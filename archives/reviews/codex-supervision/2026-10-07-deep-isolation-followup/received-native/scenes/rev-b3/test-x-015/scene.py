from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'P=\\begin{pmatrix}\\frac12&\\frac12\\\\\\frac14&\\frac34\\end{pmatrix}',
            'P^n',
            'n',
            'n\\to\\infty',
            '\\lambda^2-\\frac54\\lambda+\\frac14=(\\lambda-1)(\\lambda-\\frac14)',
            '(1,1)^T',
            '(2,-1)^T',
            'Q=\\begin{pmatrix}1&2\\\\1&-1\\end{pmatrix}',
            'Q^{-1}=\\begin{pmatrix}\\frac13&\\frac23\\\\\\frac13&-\\frac13\\end{pmatrix}',
            'P=Q\\operatorname{diag}(1,\\frac14)Q^{-1}',
            'P^n=Q\\operatorname{diag}(1,4^{-n})Q^{-1}=\\frac13\\begin{pmatrix}1+2\\cdot4^{-n}&2-2\\cdot4^{-n}\\\\1-4^{-n}&2+4^{-n}\\end{pmatrix}',
            '4^{-n}\\to0',
            '\\lim_{n\\to\\infty}P^n=\\begin{pmatrix}\\frac13&\\frac23\\\\\\frac13&\\frac23\\end{pmatrix}',
            'P^n=\\frac13\\begin{pmatrix}1+2\\cdot4^{-n}&2-2\\cdot4^{-n}\\\\1-4^{-n}&2+4^{-n}\\end{pmatrix}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
