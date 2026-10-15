from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'y=\\ln(x+\\sqrt{x^2+a^2})',
            'a>0',
            "y'=\\dfrac{1+\\dfrac{x}{\\sqrt{x^2+a^2}}}{x+\\sqrt{x^2+a^2}}=\\dfrac{\\sqrt{x^2+a^2}+x}{\\sqrt{x^2+a^2}\\cdot(x+\\sqrt{x^2+a^2})}=\\dfrac{1}{\\sqrt{x^2+a^2}}",
            'e^y=x+\\sqrt{x^2+a^2}',
            'x=(e^{2y}-a^2)/(2e^y)=(e^y-a^2e^{-y})/2=a\\sinh(y-\\ln a)',
            '\\sqrt{x^2+a^2}=(e^y+a^2e^{-y})/2',
            'x\\to\\pm\\infty',
            'y\\to\\pm\\infty',
            '\\mathbb R',
            "y'=\\dfrac{1}{\\sqrt{x^2+a^2}}",
            'x=a\\sinh(y-\\ln a)=\\dfrac{e^y-a^2e^{-y}}{2}',
            'x+\\sqrt{x^2+a^2}',
            '\\sqrt{x^2+a^2}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
