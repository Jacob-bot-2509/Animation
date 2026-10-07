from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'Ax=0',
            '\\mathbb R^n',
            'n-\\mathrm{rank}(A)',
            'Ax=b',
            'b\\neq0',
            '\\eta_0+\\ker A',
            '\\ker A',
            'n-\\operatorname{rank}A',
            'x_0',
            'A(x-x_0)=0',
            'x_0+\\ker A',
            'b\\ne0',
            'b=0',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
