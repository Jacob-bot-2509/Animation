from manim import *
FORMULAS = ['f(x)=x^5+x+1', 'f(x)', 'x-1', 'x^2+1', 'ax+b', 'f(x)=(x^2+1)q(x)+ax+b', 'x=i', 'x=-i', 'f(i)=1+2i', 'f(-i)=(-i)^5-i+1=-i-i+1=1-2i', '\\begin{cases}ai+b=1+2i\\\\-ai+b=1-2i\\end{cases}', '2b=2', 'b=1', '2ai=4i', 'a=2', '2x+1', 'f(1)=1+1+1=3', '3', 'x=\\pm i', 'ai+b=1+2i']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
