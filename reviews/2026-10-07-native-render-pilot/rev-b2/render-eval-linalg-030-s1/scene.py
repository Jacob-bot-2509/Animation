from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '(1,1,0),(1,0,1),(0,1,1)',
            'u_1=(1,1,0)',
            'u_2=(1,0,1)-\\dfrac{(1,0,1)\\cdot u_1}{\\|u_1\\|^2}u_1=(1,0,1)-\\dfrac{1}{2}(1,1,0)=\\left(\\dfrac{1}{2},-\\dfrac{1}{2},1\\right)',
            'u_2=(1,-1,2)',
            'u_3=(0,1,1)-\\dfrac{(0,1,1)\\cdot u_1}{\\|u_1\\|^2}u_1-\\dfrac{(0,1,1)\\cdot u_2}{\\|u_2\\|^2}u_2=(0,1,1)-\\dfrac{1}{2}(1,1,0)-\\dfrac{1}{6}(1,-1,2)=\\left(-\\dfrac{2}{3},\\dfrac{2}{3},\\dfrac{2}{3}\\right)',
            '-\\dfrac{3}{2}',
            'u_3=(1,-1,-1)',
            'u_1\\cdot u_2=0',
            'u_1\\cdot u_3=1-1+0=0',
            'u_2\\cdot u_3=1+1-2=0',
            'u_1=(1,1,0),\\ u_2=(1,-1,2),\\ u_3=(1,-1,-1)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
