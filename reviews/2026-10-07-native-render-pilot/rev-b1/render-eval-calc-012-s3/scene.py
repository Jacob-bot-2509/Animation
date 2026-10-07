from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            '\\tan 15^\\circ',
            'ABC',
            '\\angle B=\\pi/2',
            'AB=\\sqrt3,\\ BC=1,\\ AC=2',
            '\\angle A=\\pi/6',
            'AD',
            'BC',
            'D',
            'BD/DC=AB/AC=\\sqrt3/2',
            'BD+DC=1',
            'BD=\\sqrt3/(2+\\sqrt3)',
            'ABD',
            '\\angle BAD=\\pi/12',
            '\\tan(\\pi/12)=BD/AB=1/(2+\\sqrt3)=2-\\sqrt3',
            '\\tan(5\\pi/12)=1/\\tan(\\pi/12)=2+\\sqrt3',
            '2-\\sqrt{3}',
            'BD/DC=\\sqrt3/2',
            '\\tan(\\pi/12)=BD/AB=2-\\sqrt3',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
