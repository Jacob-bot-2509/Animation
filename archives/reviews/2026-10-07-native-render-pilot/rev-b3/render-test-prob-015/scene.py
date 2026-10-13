from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'X,Y',
            '\\operatorname{Geom}\\!\\left(\\dfrac{1}{2}\\right)',
            'P(X=k)=P(Y=k)=\\left(\\dfrac{1}{2}\\right)^k',
            'P(X=Y)=\\displaystyle\\sum_{k=1}^{\\infty}P(X=k)P(Y=k)=\\sum_{k=1}^{\\infty}\\left(\\dfrac{1}{2}\\right)^{2k}=\\sum_{k=1}^{\\infty}\\left(\\dfrac{1}{4}\\right)^k=\\dfrac{1/4}{1-1/4}=\\dfrac{1}{3}',
            '\\dfrac{1}{3}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
