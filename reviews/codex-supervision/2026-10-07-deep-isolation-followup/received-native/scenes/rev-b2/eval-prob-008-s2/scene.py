from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'X\\sim B\\!\\left(100,\\dfrac{1}{2}\\right)',
            'P(|X-50|\\ge 10)',
            '\\binom{100}{k}=\\binom{100}{100-k}',
            'q=P(X\\le40)+P(X\\ge60)=\\frac{2}{2^{100}}\\sum_{k=0}^{40}\\binom{100}{k}',
            'E(X)=50',
            '\\operatorname{Var}(X)=25',
            '1/4',
            'S=\\sum_{k=0}^{40}\\binom{100}{k}',
            '\\frac14-q=\\frac{2^{97}-S}{2^{99}}',
            'E((X-50)^2)>100P(|X-50|\\ge10)',
            'X=0',
            '\\frac14',
            '\\frac{1}{2^{99}}\\sum_{k=0}^{40}\\binom{100}{k}',
            '|X-50|<10',
            'P(X\\ge60)=P(X\\le40)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
