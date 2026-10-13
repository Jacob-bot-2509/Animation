from manim import *
FORMULAS = ['f(x,y)=x^2+y^2-xy+x+y', 'f_x=2x-y+1=0', 'f_y=2y-x+1=0', 'x+y+2=0', '3x-3y=0', 'x=y', '2x=-2', 'x=y=-1', '(-1,-1)', 'H=\\begin{pmatrix}2&-1\\\\-1&2\\end{pmatrix}', '2>0', '\\det H=3>0', 'f(-1,-1)=1+1-1-1-1=-1', 'u=x+1,\\ v=y+1', 'f=-1+u^2+v^2-uv=-1+\\frac12[(u-v)^2+u^2+v^2]', 'f\\ge-1', 'u=v=0', 'y=-1,x\\to\\infty', '-1', 'z=f(x,y)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
