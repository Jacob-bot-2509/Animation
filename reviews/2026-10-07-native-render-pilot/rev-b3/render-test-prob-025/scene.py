from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'X',
            'Y',
            'X=6',
            'Z',
            'E[Y]=E[X]+E[\\mathbf 1_{\\{X=6\\}}Z]=E[X]+P(X=6)E[Z]=\\dfrac{7}{2}+\\dfrac{1}{6}\\cdot\\dfrac{7}{2}=\\dfrac{7}{2}\\left(1+\\dfrac{1}{6}\\right)=\\dfrac{7}{2}\\cdot\\dfrac{7}{6}=\\dfrac{49}{12}',
            '\\dfrac{49}{12}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
