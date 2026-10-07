from manim import *
FORMULAS = ['n', 'D_n=\\begin{vmatrix}1&1&0&\\cdots&0\\\\1&1&1&\\cdots&0\\\\0&1&1&\\cdots&0\\\\\\vdots&&&\\ddots&\\vdots\\\\0&0&\\cdots&1&1\\end{vmatrix}', 'a_{ii}=a_{i,i+1}=a_{i+1,i}=1', 'D_n=D_{n-1}-D_{n-2}', '1\\cdot D_{n-1}-1\\cdot\\begin{vmatrix}1&1&0&\\cdots\\\\0&1&1&\\cdots\\\\\\vdots\\end{vmatrix}', 'D_{n-2}', 'D_1=1', 'D_2=\\begin{vmatrix}1&1\\\\1&1\\end{vmatrix}=0', 'D_3=D_2-D_1=-1', 'D_4=D_3-D_2=-1', 'D_5=D_4-D_3=0', 'D_6=D_5-D_4=1', '1,0,-1,-1,0,1', 'D_n=D_{n-6}', 'D_{n+6}=D_{n+5}-D_{n+4}=\\cdots=D_n', 'D_{n+2}=D_{n+1}-D_n', 'D_{n+3}=D_{n+2}-D_{n+1}=-D_n', 'D_{n+6}=-D_{n+3}=D_n', '(1,0),(0,-1),(-1,-1),(-1,0),(0,1),(1,1)', 'D_1,\\dots,D_6=1,0,-1,-1,0,1']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
