from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'X\\sim B\\!\\left(100,\\dfrac{1}{2}\\right)',
            'P(|X-50|\\ge 10)',
            'E(X)=50',
            '\\operatorname{Var}(X)=100\\cdot\\frac12\\cdot\\frac12=25',
            'q=P(|X-50|\\ge10)\\le25/10^2=1/4',
            'X',
            '50',
            'q=P(X\\le40)+P(X\\ge60)=2^{-99}\\sum_{k=0}^{40}\\binom{100}{k}',
            'Y=(X-50)^2',
            'Y\\ge100',
            'P(X=0)>0',
            'Y>100',
            '25=E(Y)>100q',
            'q<1/4',
            '\\frac14',
            'q=2^{-99}\\sum_{k=0}^{40}\\binom{100}{k}<\\frac14',
            '\\dfrac{25}{100}=\\dfrac{1}{4}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
