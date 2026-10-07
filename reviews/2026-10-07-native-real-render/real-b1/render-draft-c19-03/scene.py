from manim import *
FORMULAS = ['x^2+y^2=1', 'z=2x', 'xy', '\\begin{cases}x^2+y^2=1\\\\ z=2x\\end{cases}', 'z', '-1\\le x\\le1', '(\\cos t,\\sin t,2\\cos t)', 'e_1=(0,1,0)', 'e_2=\\frac{(1,0,2)}{\\sqrt5}', '(2,0,-1)', '\\xi=e_1\\cdot(x,y,z)=y', '\\eta=e_2\\cdot(x,y,z)=(x+2z)/\\sqrt5', '(\\xi,\\eta)=(\\sin t,\\sqrt5\\cos t)', '\\xi^2+\\frac{\\eta^2}{5}=1', 'y', 'e_1', '1', '2', '(1,0,2)', 'e_2', '\\sqrt5', '2\\sqrt5']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
