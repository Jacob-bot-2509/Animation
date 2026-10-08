from manim import *
FORMULAS = ['X', 'Y', 'X=6', 'Z', 'E[Y]=E[X]+E[\\mathbf 1_{\\{X=6\\}}Z]=E[X]+P(X=6)E[Z]=\\dfrac{7}{2}+\\dfrac{1}{6}\\cdot\\dfrac{7}{2}=\\dfrac{7}{2}\\left(1+\\dfrac{1}{6}\\right)=\\dfrac{7}{2}\\cdot\\dfrac{7}{6}=\\dfrac{49}{12}', '\\dfrac{49}{12}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
