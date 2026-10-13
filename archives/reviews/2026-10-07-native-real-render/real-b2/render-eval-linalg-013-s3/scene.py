from manim import *
FORMULAS = ['x_1+x_2+x_3+x_4=0', '\\mathbb R^4', '(1,1,1,1)', '4-1=3', '\\xi_1=(1,-1,0,0)^T,\\xi_2=(1,0,-1,0)^T,\\xi_3=(1,0,0,-1)^T', 'x', 'x_1=-x_2-x_3-x_4', 'x=-x_2\\xi_1-x_3\\xi_2-x_4\\xi_3', '\\xi_1=(1,-1,0,0)^T', '\\xi_2=(1,0,-1,0)^T', '\\xi_3=(1,0,0,-1)^T', 'x=c_1\\xi_1+c_2\\xi_2+c_3\\xi_3']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
