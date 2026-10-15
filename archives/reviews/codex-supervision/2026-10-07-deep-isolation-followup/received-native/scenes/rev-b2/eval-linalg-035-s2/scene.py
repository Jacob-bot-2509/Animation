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
            'A^TA=I\\iff',
            'x',
            '|Ax|^2=(Ax)^T(Ax)=x^TA^TAx=x^Tx=|x|^2',
            '(Ax,Ay)=\\dfrac{|A(x+y)|^2-|Ax|^2-|Ay|^2}{2}=\\dfrac{|x+y|^2-|x|^2-|y|^2}{2}=(x,y)',
            'x=e_i',
            'y=e_j',
            '(Ae_i,Ae_j)=(e_i,e_j)=\\delta_{ij}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
