from manim import *
FORMULAS = ['x=a\\cos^3 t', 'y=a\\sin^3 t', 'a>0', '0\\le t\\le 2\\pi', '\\dfrac{dy}{dx}', '\\dfrac{d^2y}{dx^2}', 'F(x,y,t)=x\\sin t+y\\cos t-a\\sin t\\cos t=0', 'F_t=0', 'x=a\\cos^3t,\\ y=a\\sin^3t', '\\sin t\\cos t\\ne0', 'F=0', '\\sin t+\\cos t\\,y^{\\prime}=0', 'y^{\\prime}=-\\tan t', 'x^{\\prime}=-3a\\cos^2t\\sin t', 'y^{\\prime\\prime}=(-\\sec^2t)/x^{\\prime}=1/(3a\\cos^4t\\sin t)', 'a\\cos t,a\\sin t', 'a', 't=k\\pi/2', 't=k\\pi', 't=\\pi/2+k\\pi', '\\dfrac{dy}{dx}=-\\tan t', '\\dfrac{d^2y}{dx^2}=\\dfrac{1}{3a\\cos^4 t\\sin t}', '\\sin t\\cos t\\ne 0', 't=k\\dfrac{\\pi}{2}', 'F=F_t=0', '\\frac{d^2y}{dx^2}', 'y^{\\prime\\prime}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
