from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '|\\vec a|=2',
            '|\\vec b|=3',
            '\\vec a',
            '\\vec b',
            '60^\\circ',
            '|\\vec a+\\vec b|',
            '|2\\vec a-\\vec b|',
            '\\vec a+\\vec b',
            '\\vec a-\\vec b',
            '\\vec a,\\vec b',
            '\\pi/3',
            '|\\vec a+\\vec b|^2=4+9+2\\cdot2\\cdot3\\cos(\\pi/3)=19',
            '2\\vec a,\\vec b',
            '2\\vec a-\\vec b',
            '|2\\vec a-\\vec b|^2=16+9-2\\cdot4\\cdot3\\cos(\\pi/3)=13',
            '|\\vec a-\\vec b|^2=4+9-2\\cdot2\\cdot3\\cos(\\pi/3)=7',
            '(\\vec a+\\vec b)\\cdot(\\vec a-\\vec b)=|\\vec a|^2-|\\vec b|^2=-5',
            '-5/\\sqrt{19\\cdot7}=-5/\\sqrt{133}',
            '|\\vec a+\\vec b|=\\sqrt{19}',
            '|2\\vec a-\\vec b|=\\sqrt{13}',
            '\\cos\\theta=-\\dfrac{5}{\\sqrt{133}}',
            '16+9-24\\cos(\\pi/3)=13',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
