from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\lim_{x \\to 0} \\frac{\\sin x}{x}',
            'x',
            '0 < x < \\frac{\\pi}{2}',
            '\\triangle OAB',
            'OAB',
            '\\triangle OAC',
            '\\sin x < x < \\tan x',
            '\\sin x',
            '1 < \\frac{x}{\\sin x} < \\frac{1}{\\cos x}',
            '\\cos x < \\frac{\\sin x}{x} < 1',
            '\\frac{\\sin x}{x}',
            'x \\to 0^-',
            'x \\to 0',
            '\\cos x \\to 1',
            '\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1',
            'O=(0,0)',
            'A=(1,0)',
            'B=(\\cos x,\\sin x)',
            '0<x<\\frac{\\pi}{2}',
            'C=(1,\\tan x)',
            'OB',
            'A',
            '\\frac12\\sin x,\\frac12 x,\\frac12\\tan x',
            'x=\\frac{\\pi}{4}',
            '\\triangle OAB\\subsetneq',
            'OAB\\subsetneq\\triangle OAC',
            '\\sin x<x<\\tan x',
            '\\sin x>0',
            '\\cos x<\\frac{\\sin x}{x}<1',
            '\\lim_{x\\to0^+}\\cos x=1',
            '\\frac{\\sin(-x)}{-x}=\\frac{\\sin x}{x}',
            '1',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
