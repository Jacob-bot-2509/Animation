from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'a\\in\\mathbb R',
            'f(x,y,z)=2x^2+y^2+2z^2+2xy+2axz',
            'a',
            '2\\left(x+\\dfrac{y}{2}+\\dfrac{az}{2}\\right)^2=2x^2+\\dfrac{y^2}{2}+\\dfrac{a^2z^2}{2}+2xy+2axz+ayz',
            'f=2\\left(x+\\frac{y}{2}+\\frac{az}{2}\\right)^2+\\left[\\frac{y^2}{2}-ayz+\\left(2-\\frac{a^2}{2}\\right)z^2\\right]=2\\left(x+\\frac{y}{2}+\\frac{az}{2}\\right)^2+\\frac{1}{2}(y-az)^2+(2-a^2)z^2.',
            ' 三项系数 ',
            ' 全正 ',
            ',与解法一一致。变量替换',
            '的矩阵为上三角且行列式1，故可逆。若',
            '，取非零向量',
            '，前两平方为零且',
            '-\\sqrt{2}<a<\\sqrt{2}',
            '2-a^2',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
