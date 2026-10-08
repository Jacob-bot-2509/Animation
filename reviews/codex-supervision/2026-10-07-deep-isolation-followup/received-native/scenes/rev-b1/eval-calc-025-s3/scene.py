from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\displaystyle\\sum_{n=2}^{\\infty}\\frac{(-1)^n}{\\ln n}',
            'a_n=1/\\ln n',
            'n\\ge2',
            'a_n\\downarrow0',
            'p\\ge2',
            'B_j=\\sum_{n=p}^j(-1)^n',
            '|B_j|\\le1',
            '\\sum_{n=p}^q(-1)^na_n=B_qa_q+\\sum_{j=p}^{q-1}B_j(a_j-a_{j+1})',
            'a_q+\\sum_{j=p}^{q-1}(a_j-a_{j+1})=a_p\\to0',
            '\\sum_{n=2}^N1/\\ln n\\ge(N-1)/\\ln N\\to\\infty',
            '\\ln N/N\\to0',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
