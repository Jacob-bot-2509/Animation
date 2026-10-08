from manim import *
FORMULAS = ['X', '\\operatorname{Var}(X)', 'X=X_1+X_2', 'X_1,X_2', '\\operatorname{Var}(X_i)=\\dfrac{35}{12}', '\\operatorname{Var}(X)=\\operatorname{Var}(X_1)+\\operatorname{Var}(X_2)=\\dfrac{35}{12}+\\dfrac{35}{12}=\\dfrac{35}{6}', 'E[X]=7', 'E[X^2]=\\displaystyle\\sum_{k=2}^{12}k^2P(X=k)=\\dfrac{1974}{36}=\\dfrac{329}{6}', '\\operatorname{Var}(X)=\\dfrac{329}{6}-49=\\dfrac{329-294}{6}=\\dfrac{35}{6}', '\\dfrac{35}{6}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
