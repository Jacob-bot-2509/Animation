from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '20',
            'h(t)=20-5t^2',
            't',
            "v(t)=h'(t)=-10t",
            "a(t)=v'(t)=-10",
            'h(t)=0',
            '20-5t^2=0',
            't=2',
            'v(2)=-20',
            'v(t)=-10t',
            'a(t)=-10',
            '^2',
            '-20',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
