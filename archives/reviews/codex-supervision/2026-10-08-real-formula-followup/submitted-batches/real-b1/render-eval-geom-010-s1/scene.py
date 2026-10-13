from manim import *
FORMULAS = ['z=xy', 'u=\\dfrac{x+y}{\\sqrt{2}}', 'v=\\dfrac{x-y}{\\sqrt{2}}', 'x=\\dfrac{u+v}{\\sqrt{2}}', 'y=\\dfrac{u-v}{\\sqrt{2}}', 'xy=\\dfrac{u^2-v^2}{2}', 'z=\\dfrac{u^2}{2}-\\dfrac{v^2}{2}', '2z=u^2-v^2', '(x,y,z)=(t,c,ct)', '(c,t,ct)', 'c,t\\in\\mathbb R', '(x_0,y_0,x_0y_0)', 'c=y_0', 'c=x_0', '45^\\circ']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
