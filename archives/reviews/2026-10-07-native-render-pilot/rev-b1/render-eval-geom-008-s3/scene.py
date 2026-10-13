from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '2x^2+y^2-z^2+4xy=1',
            'z=0',
            '2x^2+4xy+y^2=1',
            '2(x+y)^2-y^2=1',
            'y=0',
            '2x^2-z^2=1',
            'x+y=0',
            'x=-y',
            '-y^2-z^2=1',
            'z',
            'x+y',
            'u=x+y,\\ v=y,\\ w=z',
            '2u^2-v^2-w^2=1',
            'u=\\pm\\sqrt{(1+v^2+w^2)/2}',
            '\\mathbb R^2',
            '|u|\\ge1/\\sqrt2',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
