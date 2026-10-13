from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'n',
            '\\bar X_n',
            'P(|\\bar X_n-\\frac72|\\ge\\frac1{10})',
            'n\\to\\infty',
            '0',
            'X_i',
            '1,\\ldots,6',
            'E(X_i)=\\frac16\\sum_{k=1}^6k=\\frac72',
            'E(X_i^2)=\\frac16\\sum_{k=1}^6k^2=\\frac{91}{6}',
            '\\operatorname{Var}(X_i)=\\frac{91}{6}-\\frac{49}{4}=\\frac{35}{12}',
            'E(\\bar X_n)=\\frac72',
            '\\operatorname{Var}(\\bar X_n)=\\frac{35}{12n}',
            'P(|\\bar X_n-\\frac72|\\ge\\frac1{10})\\le\\min\\{1,\\frac{35}{12n}\\cdot100\\}=\\min\\{1,\\frac{875}{3n}\\}',
            '\\min\\{1,\\frac{875}{3n}\\}',
            'E(X_i)=7/2',
            '\\operatorname{Var}(X_i)=35/12',
            '\\operatorname{Var}(\\overline X_n)=35/(12n)',
            '1/10',
            'P(|\\overline X_n-7/2|\\ge1/10)\\le\\min\\{1,875/(3n)\\}\\to0',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
