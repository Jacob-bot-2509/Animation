from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '(1,1,0),(1,0,1),(0,1,1)',
            '\\begin{vmatrix}1&1&0\\\\1&-1&2\\\\1&-1&-1\\end{vmatrix}=1\\cdot(1+2)-1\\cdot(-1-2)+0=3+3=6\\ne 0',
            '\\begin{vmatrix}1&1&0\\\\1&0&1\\\\0&1&1\\end{vmatrix}=-2\\ne 0',
            '\\mathbb R^3',
            'v_1=(1,1,0),v_2=(1,0,1),v_3=(0,1,1)',
            'w_1=v_1',
            'w_2=v_2-\\frac{\\langle v_2,w_1\\rangle}{\\langle w_1,w_1\\rangle}w_1=(1/2,-1/2,1)',
            'u_2=(1,-1,2)',
            'w_3=v_3-\\frac12w_1-\\frac16u_2=(-2/3,2/3,2/3)',
            'u_3=(-3/2)w_3=(1,-1,-1)',
            'u_1=(1,1,0),u_2=(1,-1,2),u_3=(1,-1,-1)',
            'u_1=(1,1,0),\\ u_2=(1,-1,2),\\ u_3=(1,-1,-1)',
            '6\\ne0',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
