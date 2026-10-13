from manim import *
FORMULAS = ['A=\\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}', 'x^2+y^2=1', 'A', '(x,y)', "(x',y')=(x+y,y)", "x=x'-y'", "y=y'", "(x'-y')^2+y'^2=1", "x'^2-2x'y'+2y'^2=1", "x'^2-2x'y'+2y'^2", '\\begin{pmatrix}1&-1\\\\-1&2\\end{pmatrix}', '1>0', '\\det A=1', '=\\pi\\cdot|\\det A|=\\pi', 'x^2-2xy+2y^2=1', '\\pi']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
