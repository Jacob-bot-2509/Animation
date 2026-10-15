from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'p,q,r\\in\\mathbb R[t]',
            '\\mathbb R[t]',
            '\\begin{cases}t x+y=p\\\\(t-1)y+z=q\\\\z=r\\end{cases}',
            'x,y,z\\in\\mathbb R[t]',
            '\\mathbb R(t)',
            'D=t(t-1)',
            'D_x=(t-1)p-q+r',
            'D_y=t(q-r)',
            'D_z=t(t-1)r',
            'z=r',
            'y=\\frac{q-r}{t-1}',
            'x=\\frac{(t-1)p-q+r}{t(t-1)}',
            'N=(t-1)p-q+r',
            't=1',
            'q(1)=r(1)',
            't=0',
            'y(0)=r(0)-q(0)',
            'p(0)=y(0)',
            'p(0)+q(0)-r(0)=0',
            'q-r',
            't-1',
            'N(1)=0',
            'N(0)=0',
            't',
            't(t-1)\\mid N',
            'x,y,z',
            '\\Delta z=0',
            '(t-1)\\Delta y=0',
            't\\Delta x=0',
            't,t-1',
            't(t-1)',
            'N(0)=N(1)=0\\Longrightarrow t(t-1)\\mid N',
            't=1,0',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
