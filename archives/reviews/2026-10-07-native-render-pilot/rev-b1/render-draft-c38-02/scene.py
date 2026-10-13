from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\mathbb R[x]_{\\le4}',
            'U',
            'V',
            '(x-1)^2',
            'U\\cap V',
            'U+V',
            'U=\\operatorname{span}(1,x^2,x^4)',
            '3',
            'V=(x-1)^2\\mathbb R[x]_{\\le2}',
            'f=a+bx^2+cx^4\\in V',
            'f(1)=f^{\\prime}(1)=0',
            'a+b+c=0,2b+4c=0',
            'f=c(x^2-1)^2',
            '3+3-1=5',
            '\\operatorname{span}\\{(x^2-1)^2\\}',
            '1',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
