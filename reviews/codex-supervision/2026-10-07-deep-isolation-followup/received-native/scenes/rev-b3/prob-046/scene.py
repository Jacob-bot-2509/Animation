from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\Omega=[0,1)\\times[0,1)',
            '1',
            'R_k=[1-2^{-(k-1)},1-2^{-k})\\times[0,1)',
            'k\\ge1',
            '\\bigcup_{k=1}^{\\infty}R_k=\\Omega',
            '\\operatorname{area}(R_k)=2^{-k}',
            'N',
            'S_N=\\sum_{k=1}^{N}2^{-k}=1-2^{-N}',
            '2^{-N}\\to0',
            '\\operatorname{area}(\\Omega)=\\sum_{k=1}^{\\infty}\\operatorname{area}(R_k)=1',
            'R_k',
            '\\bigcup_{k=1}^\\infty R_k=[0,1)^2',
            '\\sum_{k=1}^\\infty\\operatorname{area}(R_k)=\\sum_{k=1}^\\infty2^{-k}=1',
            '\\Omega=[0,1)^2',
            'k',
            '\\Omega',
            '2^{-k}',
            'S_N=\\sum_{k=1}^N2^{-k}=1-2^{-N}',
            '\\sum_{k=1}^\\infty\\operatorname{area}(R_k)=1',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
