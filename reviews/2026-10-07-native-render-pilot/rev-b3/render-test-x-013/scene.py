from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '1',
            'N',
            'N\\to\\infty',
            '\\{1,\\ldots,N\\}',
            '\\lfloor N/2\\rfloor,\\lfloor N/3\\rfloor,\\lfloor N/6\\rfloor',
            'p_N=[\\lfloor N/2\\rfloor+\\lfloor N/3\\rfloor-\\lfloor N/6\\rfloor]/N',
            '|\\lfloor u\\rfloor-u|<1',
            '|p_N-(1/2+1/3-1/6)|<3/N\\to0',
            '2/3',
            '\\dfrac{2}{3}',
            '\\lfloor N/2\\rfloor+\\lfloor N/3\\rfloor-\\lfloor N/6\\rfloor',
            '|p_N-2/3|<3/N',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
