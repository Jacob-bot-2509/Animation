from manim import *
FORMULAS = ['\\begin{cases} 2x + y = 5 \\\\ x - y = 1 \\end{cases}', 'D=\\begin{vmatrix} 2 & 1 \\\\ 1 & -1 \\end{vmatrix}=-3\\neq0', 'D_x=\\begin{vmatrix} 5 & 1 \\\\ 1 & -1 \\end{vmatrix}=-6', 'D_y=\\begin{vmatrix} 2 & 5 \\\\ 1 & 1 \\end{vmatrix}=-3', 'x=2, y=1', 'D=0', '2x+y=5', 'x-y=1', '(2,1)', 'D=-3,\\ D_x=-6,\\ D_y=-3', 'x=D_x/D=2,\\ y=D_y/D=1', 'x+y=1,\\ 2x+2y=3', 'x+y=1,\\ 2x+2y=2', '\\{(t,1-t):t\\in\\mathbb R\\}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
