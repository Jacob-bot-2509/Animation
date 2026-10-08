from manim import *
FORMULAS = ['N=\\sum_{1\\le i<j\\le30}I_{ij}', 'I_{ij}', 'i,j', '\\binom{30}{2}=435', 'E(N)=435/365=87/73', '1/365^2', 'E(N^2)=435/365+435\\cdot434/365^2', 'E(N)^2=E(N\\mathbf1_{\\{N>0\\}})^2\\le E(N^2)P(N>0)', 'P(N>0)\\ge435/799>1/2', 'P(N>0)=1-\\frac{365!}{335!\\,365^{30}}', '1-\\frac{365!}{335!\\,365^{30}}', 'N=\\sum_{i<j}I_{ij}', '435', 'P(N>0)\\ge E(N)^2/E(N^2)=435/799>1/2', 'P(N>0)=1-365!/(335!\\,365^{30})']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
