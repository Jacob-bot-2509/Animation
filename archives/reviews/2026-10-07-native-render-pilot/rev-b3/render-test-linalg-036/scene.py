from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'k',
            'k\\ne0',
            'P_{ij}',
            '\\det P_{ij}=-1',
            'i',
            'D_i(k)',
            '\\det D_i(k)=k',
            'j',
            'E_{ij}',
            '\\det E_{ij}=1',
            'B',
            '\\det(P_{ij}B)=-\\det B',
            '\\det(D_i(k)B)=k\\det B',
            '\\det(E_{ij}B)=\\det B',
            '-1',
            '1',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
