from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'A',
            '365^{30}',
            '365\\cdot364\\cdots336=365!/335!',
            'P(A^c)=\\frac{365!}{335!\\,365^{30}}',
            'P(A)=1-\\frac{365!}{335!\\,365^{30}}',
            '1-\\frac{365!}{335!\\,365^{30}}',
            '\\dfrac{365\\cdot364\\cdots336}{365^{30}}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
