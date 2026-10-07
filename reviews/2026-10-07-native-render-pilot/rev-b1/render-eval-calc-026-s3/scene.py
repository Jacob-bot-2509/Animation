from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'z=x^y',
            'x>0',
            'z',
            '(1,2)',
            'z_x(1,2)=\\lim_{h\\to0}\\frac{(1+h)^2-1}{h}=\\lim_{h\\to0}(2+h)=2',
            'h\\ne0',
            '1+h>0',
            'z_y(1,2)=\\lim_{h\\to0}\\frac{1^{2+h}-1}{h}=\\lim_{h\\to0}0=0',
            'z_x(1,2)=2',
            'z_y(1,2)=0',
            'x',
            '((1+h)^2-1)/h=2+h',
            'h\\to0',
            'y',
            '(1^{2+h}-1)/h=0',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
