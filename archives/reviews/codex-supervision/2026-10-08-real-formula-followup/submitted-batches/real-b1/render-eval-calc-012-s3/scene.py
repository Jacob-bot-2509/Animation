from manim import *
FORMULAS = ['\\tan 15^\\circ', 'ABC', '\\angle B=\\pi/2', 'AB=\\sqrt3,\\ BC=1,\\ AC=2', '\\angle A=\\pi/6', 'AD', 'BC', 'D', 'BD/DC=AB/AC=\\sqrt3/2', 'BD+DC=1', 'BD=\\sqrt3/(2+\\sqrt3)', 'ABD', '\\angle BAD=\\pi/12', '\\tan(\\pi/12)=BD/AB=1/(2+\\sqrt3)=2-\\sqrt3', '\\tan(5\\pi/12)=1/\\tan(\\pi/12)=2+\\sqrt3', '2-\\sqrt{3}', 'BD/DC=\\sqrt3/2', '\\tan(\\pi/12)=BD/AB=2-\\sqrt3']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
