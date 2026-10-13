from manim import *
FORMULAS = ['l:x=1+t,\\ y=t,\\ z=t', 'x^2+y^2+z^2=4', 'O(0,0,0)', 'P_0(1,0,0)', '\\vec s=(1,1,1)', '\\overrightarrow{P_0O}=(-1,0,0)', '\\overrightarrow{P_0O}\\times\\vec s=(0\\cdot 1-0\\cdot 1,\\ 0\\cdot 1-(-1)\\cdot 1,\\ (-1)\\cdot 1-0\\cdot 1)=(0,1,-1)', '\\sqrt{2}', 'd=\\dfrac{\\sqrt{2}}{\\sqrt{3}}=\\sqrt{\\dfrac{2}{3}}<2', '=2\\sqrt{4-\\dfrac{2}{3}}=2\\sqrt{\\dfrac{10}{3}}', '|t_1-t_2|\\cdot|\\vec s|=\\dfrac{2\\sqrt{10}}{3}\\cdot\\sqrt{3}=2\\sqrt{\\dfrac{10}{3}}', 'r(t)=(1+t,t,t)', 'd=(1,1,1)', 'r(t)\\cdot d=1+3t=0', 't_0=-1/3', 'Q=(2/3,-1/3,-1/3)', '|r(t)|^2=|Q|^2+|d|^2(t-t_0)^2=2/3+3(t+1/3)^2', '4', 't=(-1\\pm\\sqrt{10})/3', 'r(t)', '\\left(\\dfrac{2+\\sqrt{10}}{3},\\dfrac{-1+\\sqrt{10}}{3},\\dfrac{-1+\\sqrt{10}}{3}\\right)', '\\left(\\dfrac{2-\\sqrt{10}}{3},\\dfrac{-1-\\sqrt{10}}{3},\\dfrac{-1-\\sqrt{10}}{3}\\right)', '\\sqrt{\\dfrac{2}{3}}', '2\\sqrt{\\dfrac{10}{3}}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
