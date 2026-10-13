from manim import *
FORMULAS = ['\\begin{vmatrix} 1 & 2 & 0 \\\\ 0 & 1 & 3 \\\\ 2 & 1 & 1 \\end{vmatrix}', '1(1\\cdot1-3\\cdot1)-2(0\\cdot1-3\\cdot2)+0=1(-2)-2(-6)=-2+12=10', 'u=(1,0,2)^T,\\ v=(2,1,1)^T,\\ w=(0,3,1)^T', 'u\\times v=(-2,3,1)^T', 'B=\\sqrt{14}', 'h=\\frac{10}{\\sqrt{14}}', 'u,v,w', '(u\\times v)\\cdot w=10', 'B=\\|u\\times v\\|=\\sqrt{14}', 'h=\\frac{|(u\\times v)\\cdot w|}{\\|u\\times v\\|}=\\frac{10}{\\sqrt{14}}', 'V=Bh=10=|\\det A|']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
