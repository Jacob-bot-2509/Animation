from manim import *
class AcceptScene(Scene):
    def construct(self):
        eq = MathTex(r'x^2 + y^2 = 1')
        self.play(Write(eq))
        self.wait(1)
