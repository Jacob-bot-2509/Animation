from manim import *
FORMULAS = ['A=\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}', '\\det A', 'A', 'A^{-1}', '\\det A=-2\\ne 0', '\\operatorname{rank}A=2', 'AA^{-1}=\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}\\begin{pmatrix}-2&1\\\\\\frac{3}{2}&-\\frac{1}{2}\\end{pmatrix}=\\begin{pmatrix}-2+3&1-1\\\\-6+6&3-2\\end{pmatrix}=\\begin{pmatrix}1&0\\\\0&1\\end{pmatrix}', '\\det A=-2', '2', 'A^{-1}=\\begin{pmatrix}-2&1\\\\\\frac{3}{2}&-\\frac{1}{2}\\end{pmatrix}', '-2']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
