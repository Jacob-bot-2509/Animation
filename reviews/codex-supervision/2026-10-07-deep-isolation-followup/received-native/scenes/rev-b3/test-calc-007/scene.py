from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'f',
            "f(0)=f'(0)=0",
            '\\displaystyle\\lim_{x\\to 0}\\frac{f(x)}{x^2}',
            'f(0)=0',
            "f'(0)=0",
            '\\dfrac{f(x)}{x^2}',
            '\\dfrac{0}{0}',
            "\\lim_{x\\to 0}\\dfrac{f'(x)}{2x}",
            "f''",
            "\\lim_{x\\to 0}\\dfrac{f'(x)}{2x}=\\dfrac{1}{2}\\lim_{x\\to 0}\\dfrac{f'(x)-f'(0)}{x}=\\dfrac{f''(0)}{2}",
            "\\dfrac{f''(0)}{2}",
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
