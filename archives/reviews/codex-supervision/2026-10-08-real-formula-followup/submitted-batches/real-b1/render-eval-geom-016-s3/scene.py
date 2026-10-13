from manim import *
FORMULAS = ['|\\vec a|=2', '|\\vec b|=3', '\\vec a', '\\vec b', '60^\\circ', '|\\vec a+\\vec b|', '|2\\vec a-\\vec b|', '\\vec a+\\vec b', '\\vec a-\\vec b', '\\vec a,\\vec b', '\\pi/3', '|\\vec a+\\vec b|^2=4+9+2\\cdot2\\cdot3\\cos(\\pi/3)=19', '2\\vec a,\\vec b', '2\\vec a-\\vec b', '|2\\vec a-\\vec b|^2=16+9-2\\cdot4\\cdot3\\cos(\\pi/3)=13', '|\\vec a-\\vec b|^2=4+9-2\\cdot2\\cdot3\\cos(\\pi/3)=7', '(\\vec a+\\vec b)\\cdot(\\vec a-\\vec b)=|\\vec a|^2-|\\vec b|^2=-5', '-5/\\sqrt{19\\cdot7}=-5/\\sqrt{133}', '|\\vec a+\\vec b|=\\sqrt{19}', '|2\\vec a-\\vec b|=\\sqrt{13}', '\\cos\\theta=-\\dfrac{5}{\\sqrt{133}}', '16+9-24\\cos(\\pi/3)=13']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
