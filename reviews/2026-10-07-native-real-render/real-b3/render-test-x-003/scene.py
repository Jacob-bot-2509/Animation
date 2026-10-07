from manim import *
FORMULAS = ['A', '\\dfrac{d}{dt}e^{tA}=Ae^{tA}', 'e^{tA}=\\displaystyle\\sum_{k=0}^{\\infty}\\dfrac{t^kA^k}{k!}', 't', '\\dfrac{d}{dt}e^{tA}=\\displaystyle\\sum_{k=1}^{\\infty}\\dfrac{kt^{k-1}A^k}{k!}=\\sum_{k=1}^{\\infty}\\dfrac{t^{k-1}A^k}{(k-1)!}=A\\sum_{m=0}^{\\infty}\\dfrac{t^mA^m}{m!}=Ae^{tA}', "X'=AX", 'X(0)=I', 'R>0', '|t|\\le R', 'R^k\\|A\\|^k/k!', 'R^{k-1}\\|A\\|^k/(k-1)!', 'k\\ge1', 'e^{R\\|A\\|}', '\\|A\\|e^{R\\|A\\|}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
