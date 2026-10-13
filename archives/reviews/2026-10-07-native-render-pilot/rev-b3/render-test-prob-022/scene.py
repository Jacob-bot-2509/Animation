from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'X',
            '\\operatorname{Var}(X)',
            'X=X_1+X_2',
            'X_1,X_2',
            '\\operatorname{Var}(X_i)=\\dfrac{35}{12}',
            '\\operatorname{Var}(X)=\\operatorname{Var}(X_1)+\\operatorname{Var}(X_2)=\\dfrac{35}{12}+\\dfrac{35}{12}=\\dfrac{35}{6}',
            'E[X]=7',
            'E[X^2]=\\displaystyle\\sum_{k=2}^{12}k^2P(X=k)=\\dfrac{1974}{36}=\\dfrac{329}{6}',
            '\\operatorname{Var}(X)=\\dfrac{329}{6}-49=\\dfrac{329-294}{6}=\\dfrac{35}{6}',
            '\\dfrac{35}{6}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
