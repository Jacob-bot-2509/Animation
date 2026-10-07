from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'y=\\ln(x+\\sqrt{x^2+a^2})',
            'a>0',
            'x=a\\sinh t',
            'x+\\sqrt{x^2+a^2}=a(\\sinh t+\\cosh t)=a e^t',
            'y=\\ln(ae^t)=t+\\ln a',
            'y=\\operatorname{arsinh}\\dfrac{x}{a}+\\ln a',
            "(\\operatorname{arsinh} u)'=\\dfrac{u'}{\\sqrt{1+u^2}}",
            "y'=\\dfrac{1/a}{\\sqrt{1+x^2/a^2}}=\\dfrac{1}{\\sqrt{x^2+a^2}}",
            'e^y=x+\\sqrt{x^2+a^2}',
            'x=(e^{2y}-a^2)/(2e^y)=(e^y-a^2e^{-y})/2=a\\sinh(y-\\ln a)',
            '\\sqrt{x^2+a^2}=(e^y+a^2e^{-y})/2',
            'x\\to\\pm\\infty',
            'y\\to\\pm\\infty',
            '\\mathbb R',
            "y'=\\dfrac{1}{\\sqrt{x^2+a^2}}",
            'x=a\\sinh(y-\\ln a)=\\dfrac{e^y-a^2e^{-y}}{2}',
            'Y^2-X^2=a^2',
            'X=a\\sinh t,\\ Y=a\\cosh t',
            '\\sinh t+\\cosh t=e^t',
            'x=a\\sinh(y-\\ln a)',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
