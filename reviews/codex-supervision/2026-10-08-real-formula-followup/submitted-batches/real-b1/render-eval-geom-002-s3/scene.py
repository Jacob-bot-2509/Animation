from manim import *
FORMULAS = ['l_1:\\dfrac{x-1}{2}=\\dfrac{y+1}{1}=\\dfrac{z-2}{-1}', 'l_2:\\dfrac{x+1}{1}=\\dfrac{y-2}{2}=\\dfrac{z}{1}', 'd_1=(2,1,-1)', 'd_2=(1,2,1)', 'd_1\\times d_2=(3,-3,3)\\ne0', '\\Delta=(-2,3,-2)', '-21\\ne0', '\\Delta', '\\operatorname{span}\\{d_1,d_2\\}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
