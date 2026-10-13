from manim import *
FORMULAS = ['\\begin{cases}x=t^2\\\\ y=t^3-3t\\end{cases}', 't=2', 't', '\\frac{dx}{dt}=2t', '\\frac{dy}{dt}=3t^2-3', '\\frac{dy}{dx}=\\frac{3t^2-3}{2t}', '(4,2)', '\\frac{12-3}{4}=\\frac{9}{4}', 'y-2=\\frac{9}{4}(x-4)', 'y=\\frac{9}{4}x-7', '\\frac{dy}{dt}=0', '\\frac{dx}{dt}\\neq 0', '3t^2-3=0', 't=\\pm 1', '(1,-2)', '(1,2)', 'y=-2', 'y=2', '\\frac{dx}{dt}=0', '\\frac{dy}{dt}\\neq 0', '2t=0', 't=0', '\\frac{dy}{dt}=-3\\neq 0', '(0,0)', 'x=0', '(2t,3t^2-3)', '2t\\ne0', 't=\\pm1', '3t^2-3\\ne0', 't,-t', 't^3-3t=-(t^3-3t)', 't=\\pm\\sqrt3', '(3,0)', 'x=t^2,\\ y=t^3-3t', '\\frac{dy}{dx}=\\frac{3t^2-3}{2t}\\quad(t\\ne0)', 't=\\pm\\sqrt{3}', '\\frac{9}{4}', 'y=\\pm 2']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
