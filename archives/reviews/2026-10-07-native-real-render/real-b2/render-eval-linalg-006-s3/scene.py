from manim import *
FORMULAS = ['A=\\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}', 'A^n', 'n', '(x,y)\\mapsto(x+y,y)', 'n\\ge0', '(x+ny,y)', 'n=0', 'x+ny', 'x+(n+1)y', 'A^n=\\begin{pmatrix}1&n\\\\0&1\\end{pmatrix}', 'J=A']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
