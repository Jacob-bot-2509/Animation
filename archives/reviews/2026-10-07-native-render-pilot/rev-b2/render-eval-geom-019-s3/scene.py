from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\pi_1:x+y+z=1',
            '\\pi_2:x+2y+3z=6',
            '(x,y,z)=(-4+t,5-2t,t)',
            '\\pi_1',
            '(-4+t)+(5-2t)+t=1',
            '\\pi_2',
            '(-4+t)+2(5-2t)+3t=-4+t+10-4t+3t=6',
            'z=t',
            'y+2t=5',
            'y=5-2t',
            'x=t-4',
            '\\dfrac{x+4}{1}=\\dfrac{y-5}{-2}=\\dfrac{z}{1}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
