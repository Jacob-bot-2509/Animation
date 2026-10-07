from manim import *
FORMULAS = ['J_m(\\lambda)', 'N=J_m(0)', '\\dim\\ker N^k=\\min(k,m)', 'Ne_1=0', 'Ne_i=e_{i-1}', 'i\\ge2', 'N^k', 'e_i', 'e_{i-k}', 'i>k', '0', 'i\\le k', 'e_1,\\dots,e_{m-k}', 'k<m', 'm-k', 'k\\ge m', 'N^k=0', '\\dim\\ker N^k=m-(m-k)=k', '\\dim\\ker N^k=m', '\\min(k,m)', 'r_k=\\dim\\ker(A-\\lambda I)^k', 'k', '\\lambda', 'r_k-r_{k-1}', 'm', 'r_k', '\\min(k,m)-\\min(k-1,m)', '\\ge k', '1', 'r_0=0,r_1,r_2,\\dots', '\\dim\\ker J_m(0)^k=\\min(k,m)', 'r_0=0', '2r_k-r_{k-1}-r_{k+1}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
