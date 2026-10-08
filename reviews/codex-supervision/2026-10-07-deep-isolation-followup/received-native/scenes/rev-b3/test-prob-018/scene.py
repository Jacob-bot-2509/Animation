from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'X\\sim\\operatorname{Exp}(\\lambda)',
            'E[e^{tX}]',
            '\\lambda>0,\\ t\\in\\mathbb R',
            'M(t)=E[e^{tX}]=\\displaystyle\\int_0^{\\infty}e^{tx}\\lambda e^{-\\lambda x}dx=\\lambda\\int_0^{\\infty}e^{(t-\\lambda)x}dx',
            't<\\lambda',
            'M(t)=\\lambda\\cdot\\dfrac{1}{\\lambda-t}=\\dfrac{\\lambda}{\\lambda-t}',
            't\\ge\\lambda',
            't=\\lambda',
            '\\int\\lambda\\,dx',
            'E[e^{tX}]=\\lambda/(\\lambda-t)',
            '+\\infty',
            't',
            '\\lambda',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
