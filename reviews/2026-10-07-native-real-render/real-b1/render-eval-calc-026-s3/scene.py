from manim import *
FORMULAS = ['z=x^y', 'x>0', 'z', '(1,2)', 'z_x(1,2)=\\lim_{h\\to0}\\frac{(1+h)^2-1}{h}=\\lim_{h\\to0}(2+h)=2', 'h\\ne0', '1+h>0', 'z_y(1,2)=\\lim_{h\\to0}\\frac{1^{2+h}-1}{h}=\\lim_{h\\to0}0=0', 'z_x(1,2)=2', 'z_y(1,2)=0', 'x', '((1+h)^2-1)/h=2+h', 'h\\to0', 'y', '(1^{2+h}-1)/h=0']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
