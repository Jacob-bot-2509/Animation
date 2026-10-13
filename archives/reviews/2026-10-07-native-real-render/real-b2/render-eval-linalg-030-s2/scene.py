from manim import *
FORMULAS = ['(1,1,0),(1,0,1),(0,1,1)', 'v_1=(1,1,0),v_2=(1,0,1),v_3=(0,1,1)', 'w_1=v_1', 'w_2=v_2-\\frac{\\langle v_2,w_1\\rangle}{\\langle w_1,w_1\\rangle}w_1=(1/2,-1/2,1)', 'u_2=(1,-1,2)', 'w_3=v_3-\\frac12w_1-\\frac16u_2=(-2/3,2/3,2/3)', 'u_3=(-3/2)w_3=(1,-1,-1)', 'u_1=(1,1,0),u_2=(1,-1,2),u_3=(1,-1,-1)', 'u_1=(1,1,0),\\ u_2=(1,-1,2),\\ u_3=(1,-1,-1)', 'w_2=v_2-\\frac12v_1', 'w_3=v_3-\\frac12v_1-\\frac16(1,-1,2)', '(1,1,0),(1,-1,2),(1,-1,-1)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
