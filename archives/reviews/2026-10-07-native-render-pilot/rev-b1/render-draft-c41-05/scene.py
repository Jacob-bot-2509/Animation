from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'J_m(\\lambda)',
            'N=J_m(0)',
            '\\dim\\ker N^k=\\min(k,m)',
            'Ne_1=0',
            'Ne_i=e_{i-1}',
            'i\\ge2',
            'N^k',
            'e_i',
            'e_{i-k}',
            'i>k',
            '0',
            'i\\le k',
            'e_1,\\dots,e_{m-k}',
            'k<m',
            'm-k',
            'k\\ge m',
            'N^k=0',
            '\\dim\\ker N^k=m-(m-k)=k',
            '\\dim\\ker N^k=m',
            '\\min(k,m)',
            'r_k=\\dim\\ker(A-\\lambda I)^k',
            'k',
            '\\lambda',
            'r_k-r_{k-1}',
            'm',
            'r_k',
            '\\min(k,m)-\\min(k-1,m)',
            '\\ge k',
            '1',
            'r_0=0,r_1,r_2,\\dots',
            '\\dim\\ker J_m(0)^k=\\min(k,m)',
            'r_0=0',
            '2r_k-r_{k-1}-r_{k+1}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
