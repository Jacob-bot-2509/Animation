from manim import *
FORMULAS = ['a\\in\\mathbb R', 'f(x,y,z)=2x^2+y^2+2z^2+2xy+2axz', 'a', '2\\left(x+\\dfrac{y}{2}+\\dfrac{az}{2}\\right)^2=2x^2+\\dfrac{y^2}{2}+\\dfrac{a^2z^2}{2}+2xy+2axz+ayz', 'f=2\\left(x+\\frac{y}{2}+\\frac{az}{2}\\right)^2+\\left[\\frac{y^2}{2}-ayz+\\left(2-\\frac{a^2}{2}\\right)z^2\\right]=2\\left(x+\\frac{y}{2}+\\frac{az}{2}\\right)^2+\\frac{1}{2}(y-az)^2+(2-a^2)z^2.', '2,\\ \\dfrac{1}{2},\\ 2-a^2', '\\iff 2-a^2>0\\iff |a|<\\sqrt{2}', 'u=x+y/2+az/2,\\ v=y-az,\\ w=z', '2-a^2\\le0', '(x,y,z)=(-a,a,1)', 'f=2-a^2\\le0', '-\\sqrt{2}<a<\\sqrt{2}', '2-a^2']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
