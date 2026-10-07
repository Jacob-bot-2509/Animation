from manim import *
FORMULAS = ['1', 'N', 'N\\to\\infty', '\\{1,\\ldots,N\\}', '\\lfloor N/2\\rfloor,\\lfloor N/3\\rfloor,\\lfloor N/6\\rfloor', 'p_N=[\\lfloor N/2\\rfloor+\\lfloor N/3\\rfloor-\\lfloor N/6\\rfloor]/N', '|\\lfloor u\\rfloor-u|<1', '|p_N-(1/2+1/3-1/6)|<3/N\\to0', '2/3', '\\dfrac{2}{3}', '\\lfloor N/2\\rfloor+\\lfloor N/3\\rfloor-\\lfloor N/6\\rfloor', '|p_N-2/3|<3/N']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
