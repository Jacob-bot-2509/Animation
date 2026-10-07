from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\vec a,\\vec b',
            '|\\vec a\\cdot\\vec b|\\le|\\vec a||\\vec b|',
            '\\vec b=\\vec 0',
            '\\vec b\\ne\\vec 0',
            '\\vec a',
            '\\vec a=\\vec a_\\parallel+\\vec a_\\perp',
            '\\vec a_\\parallel=\\dfrac{\\vec a\\cdot\\vec b}{|\\vec b|^2}\\vec b',
            '\\vec b',
            '\\vec a_\\perp\\perp\\vec b',
            '|\\vec a|^2=|\\vec a_\\parallel|^2+|\\vec a_\\perp|^2\\ge|\\vec a_\\parallel|^2=\\dfrac{(\\vec a\\cdot\\vec b)^2}{|\\vec b|^2}',
            '\\vec a_\\perp=\\vec 0',
            '|\\vec a|^2\\ge|\\vec a_\\parallel|^2',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
