from manim import *
FORMULAS = ['\\vec a,\\vec b', '|\\vec a\\cdot\\vec b|\\le|\\vec a||\\vec b|', '\\vec a,\\vec b\\in\\mathbb R^n', '\\{1,\\ldots,n\\}', 'X(i)=a_i,\\ Y(i)=b_i', 'E[X^2]=|\\vec a|^2/n', 'E[Y^2]=|\\vec b|^2/n', 'E[XY]=(\\vec a\\cdot\\vec b)/n', 'E[Y^2]=0', '\\vec b=0', 'E[(X-tY)^2]\\ge0', 't=E[XY]/E[Y^2]', 'E[X^2]-(E[XY])^2/E[Y^2]\\ge0', 'X=tY']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
