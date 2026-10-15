from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'x = a(t - \\sin t), y = a(1 - \\cos t)',
            '0 \\le t \\le 2\\pi',
            'x',
            'a>0',
            'S = \\int_{0}^{2\\pi a} y dx',
            'S = \\int_{0}^{2\\pi} a(1 - \\cos t) \\cdot d[a(t - \\sin t)] = \\int_{0}^{2\\pi} a(1 - \\cos t) \\cdot a(1 - \\cos t) dt = a^2 \\int_{0}^{2\\pi} (1 - 2\\cos t + \\cos^2 t) dt',
            '\\cos t',
            'S = a^2 \\int_{0}^{2\\pi} (1 + \\frac{1+\\cos 2t}{2}) dt = a^2 \\cdot 3\\pi = 3\\pi a^2',
            '3\\pi a^2',
            'y',
            'dx',
            't',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
