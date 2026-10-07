from manim import *
FORMULAS = ['D=\\begin{vmatrix}1&1&1&1\\\\1&2&1&1\\\\1&1&3&1\\\\1&1&1&4\\end{vmatrix}', '\\begin{vmatrix}0&0&0&-3\\\\0&1&0&-3\\\\0&0&2&-3\\\\1&1&1&4\\end{vmatrix}', 'D=(-1)^{4+1}\\cdot 1\\cdot\\begin{vmatrix}0&0&-3\\\\1&0&-3\\\\0&2&-3\\end{vmatrix}=-\\left[0-0+(-3)\\begin{vmatrix}1&0\\\\0&2\\end{vmatrix}\\right]=-(-3\\cdot 2)=6', '6']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
