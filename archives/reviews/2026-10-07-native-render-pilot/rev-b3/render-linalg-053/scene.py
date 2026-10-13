from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\begin{vmatrix} 1 & 2 & 0 \\\\ 0 & 1 & 3 \\\\ 2 & 1 & 1 \\end{vmatrix}',
            '1(1\\cdot1-3\\cdot1)-2(0\\cdot1-3\\cdot2)+0=1(-2)-2(-6)=-2+12=10',
            'u=(1,0,2)^T,\\ v=(2,1,1)^T,\\ w=(0,3,1)^T',
            'u\\times v=(-2,3,1)^T',
            'B=\\sqrt{14}',
            'h=\\frac{10}{\\sqrt{14}}',
            'u,v,w',
            '(u\\times v)\\cdot w=10',
            'B=\\|u\\times v\\|=\\sqrt{14}',
            'h=\\frac{|(u\\times v)\\cdot w|}{\\|u\\times v\\|}=\\frac{10}{\\sqrt{14}}',
            'V=Bh=10=|\\det A|',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
