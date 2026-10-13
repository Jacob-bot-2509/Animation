from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'A=\\begin{pmatrix}\\cos\\theta&-\\sin\\theta\\\\\\sin\\theta&\\cos\\theta\\end{pmatrix}',
            'A^n',
            'n\\in\\mathbb Z_{\\ge0}',
            'n=0',
            'A^0=I',
            'A',
            'z\\mapsto e^{i\\theta}z',
            '(x,y)\\mapsto(x\\cos\\theta-y\\sin\\theta,\\ x\\sin\\theta+y\\cos\\theta)',
            'e^{i\\theta}(x+iy)',
            '(e^{i\\theta})^n=e^{in\\theta}',
            'A^n=',
            'n\\theta',
            'A^n=\\begin{pmatrix}\\cos n\\theta&-\\sin n\\theta\\\\\\sin n\\theta&\\cos n\\theta\\end{pmatrix}',
            'e^{i\\theta}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
