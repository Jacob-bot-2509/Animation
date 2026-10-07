from manim import *
FORMULAS = ['y', '\\varphi', 'R_y(\\varphi)', "x'=x\\cos\\varphi+z\\sin\\varphi", "y'=y", "z'=-x\\sin\\varphi+z\\cos\\varphi", 'R_y(\\varphi)=\\begin{pmatrix}\\cos\\varphi&0&\\sin\\varphi\\\\0&1&0\\\\-\\sin\\varphi&0&\\cos\\varphi\\end{pmatrix}', 'R^TR=I', '0', '\\cos\\varphi\\sin\\varphi-\\sin\\varphi\\cos\\varphi=0', '\\cos^2\\varphi+\\sin^2\\varphi=1', '1', 'R', '\\det R=1']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
