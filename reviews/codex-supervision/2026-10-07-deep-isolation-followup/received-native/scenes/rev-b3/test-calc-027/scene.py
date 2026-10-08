from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'e^x=2x+1',
            'f(x)=e^x-2x-1',
            "f'(x)=e^x-2",
            'f',
            '(-\\infty,\\ln2)',
            '(\\ln2,+\\infty)',
            'f(0)=0',
            '\\ln2=\\int_1^2t^{-1}\\,dt>1/2',
            'f(\\ln2)=1-2\\ln2<0',
            'e^2>1+2+2=5',
            'f(2)>0',
            '0<\\ln2<1',
            '0',
            '\\xi',
            '(\\ln2,2)',
            '\\xi\\in(\\ln2,2)',
            'y=e^x',
            'y=2x+1',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
