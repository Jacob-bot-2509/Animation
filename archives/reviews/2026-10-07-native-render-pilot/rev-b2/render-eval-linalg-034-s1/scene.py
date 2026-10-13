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
            't',
            '0\\le|\\vec a+t\\vec b|^2=|\\vec a|^2+2t(\\vec a\\cdot\\vec b)+t^2|\\vec b|^2',
            '\\Delta=4(\\vec a\\cdot\\vec b)^2-4|\\vec a|^2|\\vec b|^2\\le 0',
            '(\\vec a\\cdot\\vec b)^2\\le|\\vec a|^2|\\vec b|^2',
            '\\vec a+t\\vec b=\\vec 0',
            '\\vec a',
            '\\vec b',
            '\\Delta\\le0',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
