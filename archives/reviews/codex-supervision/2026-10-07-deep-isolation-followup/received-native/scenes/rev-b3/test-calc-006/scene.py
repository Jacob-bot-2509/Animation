from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'f(x)=\\ln(1+x)',
            'f^{(n)}(0)',
            "f'(x)=(1+x)^{-1}",
            "f''(x)=-(1+x)^{-2}",
            "f'''(x)=2(1+x)^{-3}",
            'f^{(4)}(x)=-6(1+x)^{-4}',
            'f^{(n)}(x)=(-1)^{n-1}(n-1)!\\,(1+x)^{-n}',
            'n\\ge 1',
            'f^{(n)}(0)=(-1)^{n-1}(n-1)!',
            '\\ln(1+x)=\\displaystyle\\sum_{n=1}^{\\infty}\\dfrac{(-1)^{n-1}x^n}{n}',
            '|x|<1',
            '1/(1+t)=\\sum_{k=0}^{\\infty}(-t)^k',
            '0',
            'x',
            'x=1',
            '1/(N+1)',
            '\\ln2',
            'x=-1',
            '|x|>1',
            '(-1,1]',
            '\\ln(1+x)=\\sum_{n=1}^{\\infty}(-1)^{n-1}x^n/n',
            '-1<x\\le1',
            'n\\ge1',
            '\\ln(1+x)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
