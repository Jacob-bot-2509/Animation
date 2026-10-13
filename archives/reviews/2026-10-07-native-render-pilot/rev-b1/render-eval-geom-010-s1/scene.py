from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'z=xy',
            'u=\\dfrac{x+y}{\\sqrt{2}}',
            'v=\\dfrac{x-y}{\\sqrt{2}}',
            'x=\\dfrac{u+v}{\\sqrt{2}}',
            'y=\\dfrac{u-v}{\\sqrt{2}}',
            'xy=\\dfrac{u^2-v^2}{2}',
            'z=\\dfrac{u^2}{2}-\\dfrac{v^2}{2}',
            '2z=u^2-v^2',
            '(x,y,z)=(t,c,ct)',
            '(c,t,ct)',
            'c,t\\in\\mathbb R',
            '(x_0,y_0,x_0y_0)',
            'c=y_0',
            'c=x_0',
            '45^\\circ',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
