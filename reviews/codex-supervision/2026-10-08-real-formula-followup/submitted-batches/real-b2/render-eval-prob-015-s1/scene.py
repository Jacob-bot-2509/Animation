from manim import *
FORMULAS = ['X', 'E[X]', '\\operatorname{Var}(X)', 'E[X]=\\dfrac{1+2+3+4+5+6}{6}=\\dfrac{21}{6}=\\dfrac{7}{2}', 'E[X^2]=\\dfrac{1+4+9+16+25+36}{6}=\\dfrac{91}{6}', '\\operatorname{Var}(X)=E[X^2]-(E[X])^2=\\dfrac{91}{6}-\\dfrac{49}{4}=\\dfrac{182-147}{12}=\\dfrac{35}{12}', 'E[X]=\\dfrac{7}{2}', '\\operatorname{Var}(X)=\\dfrac{35}{12}', '\\dfrac72', 'E[X^2]=\\dfrac{91}{6}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
