from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'N=\\sum_{1\\le i<j\\le30}I_{ij}',
            'I_{ij}',
            'i,j',
            '\\binom{30}{2}=435',
            'E(N)=435/365=87/73',
            '1/365^2',
            'E(N^2)=435/365+435\\cdot434/365^2',
            'E(N)^2=E(N\\mathbf1_{\\{N>0\\}})^2\\le E(N^2)P(N>0)',
            'P(N>0)\\ge435/799>1/2',
            'P(N>0)=1-\\frac{365!}{335!\\,365^{30}}',
            '1-\\frac{365!}{335!\\,365^{30}}',
            'N=\\sum_{i<j}I_{ij}',
            '435',
            'P(N>0)\\ge E(N)^2/E(N^2)=435/799>1/2',
            'P(N>0)=1-365!/(335!\\,365^{30})',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
