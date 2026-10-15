from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'x^8-1',
            'x^8-1=(x^4-1)(x^4+1)=(x^2-1)(x^2+1)(x^4+1)=(x-1)(x+1)(x^2+1)(x^4+1)',
            'x^4+1',
            'x^4+1=(x^2-\\sqrt2x+1)(x^2+\\sqrt2x+1)',
            '(x-1)(x+1)(x^2+1)(x^2-\\sqrt2x+1)(x^2+\\sqrt2x+1)',
            'e^{2\\pi ik/8}',
            'k=0,\\ldots,7',
            'x^8-1=\\prod_{k=0}^7(x-e^{2\\pi ik/8})',
            '-4,-2,-2',
            '\\displaystyle\\prod_{k=0}^{7}\\left(x-e^{2\\pi ik/8}\\right)',
            '(x^4-1)(x^4+1)\\to\\cdots',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
