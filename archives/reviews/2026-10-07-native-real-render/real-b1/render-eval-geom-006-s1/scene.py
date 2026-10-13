from manim import *
FORMULAS = ['\\pi_1:x+y+z=1', '\\pi_2:x-y+z=1', '\\pi_3:2x+2z=2', '\\begin{pmatrix}1&1&1&1\\\\1&-1&1&1\\\\2&0&2&2\\end{pmatrix}\\to\\begin{pmatrix}1&1&1&1\\\\0&-2&0&0\\\\0&-2&0&0\\end{pmatrix}\\to\\begin{pmatrix}1&1&1&1\\\\0&1&0&0\\\\0&0&0&0\\end{pmatrix}', '\\mathrm r(A)=\\mathrm r(\\bar A)=2<3', 'y=0', 'x+z=1', 'y=0,\\ x+z=1', '2<3']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
