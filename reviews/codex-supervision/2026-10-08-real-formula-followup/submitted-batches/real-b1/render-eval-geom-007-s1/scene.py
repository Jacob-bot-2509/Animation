from manim import *
FORMULAS = ['4x^2-y^2+z^2=1', '\\dfrac{x^2}{1/4}+\\dfrac{z^2}{1}-\\dfrac{y^2}{1}=1', '\\dfrac{x^2}{a^2}+\\dfrac{z^2}{b^2}-\\dfrac{y^2}{c^2}=1', 'y', 'y=k', '4x^2+z^2=1+k^2', 'z=k', '4x^2-y^2=1-k^2', '|k|<1', 'x', '|k|>1', '|k|=1', 'y=\\pm2x', 'x=k', 'z^2-y^2=1-4k^2', '|k|<1/2', 'z', '|k|>1/2', '|k|=1/2', 'z=\\pm y', 'k=\\pm1', 'k=\\pm1/2']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
