from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'X_1,X_2,\\ldots',
            'E(X_i)=\\mu',
            '0<\\operatorname{Var}(X_i)=\\sigma^2<\\infty',
            '\\overline X_n=n^{-1}\\sum_{i=1}^nX_i',
            '\\overline X_n',
            '\\overline X_n=\\frac{1}{n}\\sum_{i=1}^n X_i',
            'Z_n=\\frac{\\sqrt n(\\overline X_n-\\mu)}{\\sigma}\\xrightarrow{d}N(0,1)',
            't\\in\\mathbb R',
            '\\lim_{n\\to\\infty}P(Z_n\\le t)=\\Phi(t)',
            'E(\\overline X_n)=\\mu',
            '\\operatorname{Var}(\\overline X_n)=\\sigma^2/n',
            '\\overline X_n\\xrightarrow{P}\\mu',
            '\\delta_\\mu',
            'n',
            '\\overline X_n\\sim N(\\mu,\\sigma^2/n)',
            '\\frac{\\sqrt n(\\overline X_n-\\mu)}\\sigma\\xrightarrow{d}N(0,1)',
            'N(\\mu,\\sigma^2)',
            'Z_n=\\sqrt n(\\overline X_n-\\mu)/\\sigma',
            'Z_n\\xrightarrow{d}N(0,1)',
            'P(Z_n\\le t)\\to\\Phi(t)',
            '\\operatorname{Var}(\\overline X_n)=\\sigma^2/n\\to0',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
