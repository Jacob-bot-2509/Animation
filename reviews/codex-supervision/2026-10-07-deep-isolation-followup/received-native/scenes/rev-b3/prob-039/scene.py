from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'Q=[-1,1]^2',
            'n\\ge1',
            'D=\\{(x,y):x^2+y^2\\le1\\}',
            'm_n',
            '\\widehat\\pi_n=4m_n/n',
            '\\widehat\\pi_n\\xrightarrow{P}\\pi',
            '4m_n/n',
            '\\pi',
            'Q',
            'I_i',
            'i',
            'D',
            'm_n=\\sum_{i=1}^n I_i',
            'P(I_i=1)=\\frac{\\pi}{4}',
            '\\widehat\\pi_n=\\frac{4m_n}{n}',
            'E(\\widehat\\pi_n)=\\pi',
            '\\operatorname{Var}(\\widehat\\pi_n)=\\frac{\\pi(4-\\pi)}{n}',
            '\\varepsilon>0',
            'P(|\\widehat\\pi_n-\\pi|\\ge\\varepsilon)\\le\\frac{\\pi(4-\\pi)}{n\\varepsilon^2}\\to0',
            '[-1,1]^2',
            'p=\\pi/4',
            '\\operatorname{Var}(\\widehat\\pi_n)=\\pi(4-\\pi)/n',
            'P(|\\widehat\\pi_n-\\pi|\\ge\\varepsilon)\\le\\pi(4-\\pi)/(n\\varepsilon^2)\\to0',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
