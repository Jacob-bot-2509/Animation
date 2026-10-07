from manim import *
FORMULAS = ['\\displaystyle\\sum_{n=2}^{\\infty}\\frac{(-1)^n}{\\ln n}', 'a_n=1/\\ln n', 'n\\ge2', 'a_n\\downarrow0', 'p\\ge2', 'B_j=\\sum_{n=p}^j(-1)^n', '|B_j|\\le1', '\\sum_{n=p}^q(-1)^na_n=B_qa_q+\\sum_{j=p}^{q-1}B_j(a_j-a_{j+1})', 'a_q+\\sum_{j=p}^{q-1}(a_j-a_{j+1})=a_p\\to0', '\\sum_{n=2}^N1/\\ln n\\ge(N-1)/\\ln N\\to\\infty', '\\ln N/N\\to0']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
