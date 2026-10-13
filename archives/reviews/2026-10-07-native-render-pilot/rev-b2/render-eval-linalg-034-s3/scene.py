from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\vec a,\\vec b',
            '|\\vec a\\cdot\\vec b|\\le|\\vec a||\\vec b|',
            '\\vec a,\\vec b\\in\\mathbb R^n',
            '\\{1,\\ldots,n\\}',
            'X(i)=a_i,\\ Y(i)=b_i',
            'E[X^2]=|\\vec a|^2/n',
            'E[Y^2]=|\\vec b|^2/n',
            'E[XY]=(\\vec a\\cdot\\vec b)/n',
            'E[Y^2]=0',
            '\\vec b=0',
            'E[(X-tY)^2]\\ge0',
            't=E[XY]/E[Y^2]',
            'E[X^2]-(E[XY])^2/E[Y^2]\\ge0',
            'X=tY',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
