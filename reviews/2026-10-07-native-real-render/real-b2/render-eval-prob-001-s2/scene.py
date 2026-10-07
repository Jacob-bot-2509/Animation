from manim import *
FORMULAS = ['C_i', 'i', 'H_2', 'P(H_2|C_3)=1', 'P(H_2|C_1)=\\dfrac{1}{2}', 'P(H_2|C_2)=0', 'P(C_i)=\\dfrac{1}{3}', 'P(C_3|H_2)=\\dfrac{P(H_2|C_3)P(C_3)}{P(H_2|C_3)P(C_3)+P(H_2|C_1)P(C_1)+P(H_2|C_2)P(C_2)}=\\dfrac{1\\cdot\\frac{1}{3}}{1\\cdot\\frac{1}{3}+\\frac{1}{2}\\cdot\\frac{1}{3}+0}=\\dfrac{1/3}{1/2}=\\dfrac{2}{3}', '\\dfrac{2}{3}', '\\dfrac{1}{3}', 'P(C_3|H_2)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
