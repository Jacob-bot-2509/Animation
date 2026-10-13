from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '4x^2-y^2+z^2=1',
            '\\dfrac{x^2}{1/4}+\\dfrac{z^2}{1}-\\dfrac{y^2}{1}=1',
            '\\dfrac{x^2}{a^2}+\\dfrac{z^2}{b^2}-\\dfrac{y^2}{c^2}=1',
            'y',
            'y=k',
            '4x^2+z^2=1+k^2',
            'z=k',
            '4x^2-y^2=1-k^2',
            '|k|<1',
            'x',
            '|k|>1',
            '|k|=1',
            'y=\\pm2x',
            'x=k',
            'z^2-y^2=1-4k^2',
            '|k|<1/2',
            'z',
            '|k|>1/2',
            '|k|=1/2',
            'z=\\pm y',
            'k=\\pm1',
            'k=\\pm1/2',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
