from manim import *
FORMULAS = ['(1,1,0),(1,0,1),(0,1,1)', 'u_1=(1,1,0)', 'u_2=(1,0,1)-\\dfrac{(1,0,1)\\cdot u_1}{\\|u_1\\|^2}u_1=(1,0,1)-\\dfrac{1}{2}(1,1,0)=\\left(\\dfrac{1}{2},-\\dfrac{1}{2},1\\right)', 'u_2=(1,-1,2)', 'u_3=(0,1,1)-\\dfrac{(0,1,1)\\cdot u_1}{\\|u_1\\|^2}u_1-\\dfrac{(0,1,1)\\cdot u_2}{\\|u_2\\|^2}u_2=(0,1,1)-\\dfrac{1}{2}(1,1,0)-\\dfrac{1}{6}(1,-1,2)=\\left(-\\dfrac{2}{3},\\dfrac{2}{3},\\dfrac{2}{3}\\right)', '-\\dfrac{3}{2}', 'u_3=(1,-1,-1)', 'u_1\\cdot u_2=0', 'u_1\\cdot u_3=1-1+0=0', 'u_2\\cdot u_3=1+1-2=0', 'u_1=(1,1,0),\\ u_2=(1,-1,2),\\ u_3=(1,-1,-1)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
