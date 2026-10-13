from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'y=x^2',
            "\\kappa(x)=\\dfrac{|y''|}{(1+y'^2)^{3/2}}=\\dfrac{2}{(1+4x^2)^{3/2}}",
            'x=0',
            '\\kappa=2',
            'R=\\dfrac{1}{2}',
            '\\kappa(x)',
            '|x|',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
