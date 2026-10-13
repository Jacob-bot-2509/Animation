from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'X',
            'E[X]',
            '\\operatorname{Var}(X)',
            'E[X]=\\dfrac{1+2+3+4+5+6}{6}=\\dfrac{21}{6}=\\dfrac{7}{2}',
            'E[X^2]=\\dfrac{1+4+9+16+25+36}{6}=\\dfrac{91}{6}',
            '\\operatorname{Var}(X)=E[X^2]-(E[X])^2=\\dfrac{91}{6}-\\dfrac{49}{4}=\\dfrac{182-147}{12}=\\dfrac{35}{12}',
            'E[X]=\\dfrac{7}{2}',
            '\\operatorname{Var}(X)=\\dfrac{35}{12}',
            '\\dfrac72',
            'E[X^2]=\\dfrac{91}{6}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
