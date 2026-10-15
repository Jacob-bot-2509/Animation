from manim import *
FORMULAS = ['P(A)=\\frac{3}{5}', 'P(B)=\\frac{2}{5}', 'P(A\\cap B)=\\frac{1}{5}', 'P(A\\mid B)', 'P(B\\mid A)', 'P(A\\mid B)=\\frac{P(A\\cap B)}{P(B)}=\\frac{1/5}{2/5}=\\frac{1}{5}\\cdot\\frac{5}{2}=\\frac{1}{2}', 'P(B\\mid A)=\\frac{P(A\\cap B)}{P(A)}=\\frac{1/5}{3/5}=\\frac{1}{5}\\cdot\\frac{5}{3}=\\frac{1}{3}', 'P(A\\mid B)=\\frac{1}{2}', 'P(B\\mid A)=\\frac{1}{3}', '[0,1)^2', '2/5,1/5,1/5,1/5', 'A\\setminus B,A\\cap B,B\\setminus A,(A\\cup B)^c', '1', 'P(A)=3/5', 'P(B)=2/5', 'P(A\\cap B)=1/5', 'B', 'P(A\\mid B)=(1/5)/(2/5)=1/2', 'A', 'P(B\\mid A)=(1/5)/(3/5)=1/3']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
