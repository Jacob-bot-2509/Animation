from manim import *
FORMULAS = ['k', 'k\\ne0', 'P_{ij}', '\\det P_{ij}=-1', 'i', 'D_i(k)', '\\det D_i(k)=k', 'j', 'E_{ij}', '\\det E_{ij}=1', 'B', '\\det(P_{ij}B)=-\\det B', '\\det(D_i(k)B)=k\\det B', '\\det(E_{ij}B)=\\det B', '-1', '1']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
