from manim import *
FORMULAS = ['\\Omega=[0,1)\\times[0,1)', '1', 'R_k=[1-2^{-(k-1)},1-2^{-k})\\times[0,1)', 'k\\ge1', '\\bigcup_{k=1}^{\\infty}R_k=\\Omega', '\\operatorname{area}(R_k)=2^{-k}', 'N', 'S_N=\\sum_{k=1}^{N}2^{-k}=1-2^{-N}', '2^{-N}\\to0', '\\operatorname{area}(\\Omega)=\\sum_{k=1}^{\\infty}\\operatorname{area}(R_k)=1', 'R_k', '\\bigcup_{k=1}^\\infty R_k=[0,1)^2', '\\sum_{k=1}^\\infty\\operatorname{area}(R_k)=\\sum_{k=1}^\\infty2^{-k}=1', '\\Omega=[0,1)^2', 'k', '\\Omega', '2^{-k}', 'S_N=\\sum_{k=1}^N2^{-k}=1-2^{-N}', '\\sum_{k=1}^\\infty\\operatorname{area}(R_k)=1']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
