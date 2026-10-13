from manim import *
FORMULAS = ['p_n\\in[0,1]', 'np_n\\to\\lambda\\in[0,+\\infty)', 'X_n\\sim B(n,p_n)', 'k\\in\\mathbb Z_{\\ge0}', 'P(X_n=k)', '\\lambda', '\\lambda=0', '\\lambda>0', 'np_n\\to\\lambda', 'p_n\\to0', 'k\\ge0', 'n\\ge k', 'P(X_n=k)=\\frac{(np_n)^k}{k!}\\prod_{j=0}^{k-1}(1-\\frac jn)(1-p_n)^n(1-p_n)^{-k}', 'k=0', '1', '0\\le u<1', '-\\frac{u}{1-u}\\le\\log(1-u)\\le-u', '-\\frac{np_n}{1-p_n}\\le n\\log(1-p_n)\\le-np_n', 'n\\log(1-p_n)\\to-\\lambda', '(1-p_n)^n\\to e^{-\\lambda}', '\\lambda^k/k!', 'P(X_n=k)\\to e^{-\\lambda}\\lambda^k/k!', 'P(X_n\\ge1)\\le E X_n=np_n\\to0', 'P(X_n=0)\\to1', 'k\\ge1', 'P(X_n=k)\\to0', '\\displaystyle\\lim_{n\\to\\infty}P(X_n=k)=\\frac{e^{-\\lambda}\\lambda^k}{k!}', '0', 'q_k=e^{-5}5^k/k!', 'n\\in\\mathbb Z,\\ n\\ge5,\\ p_n=5/n', 'n=10', 'p_n=\\frac12', '\\binom nk(5/n)^k(1-5/n)^{n-k}', 'n', 'p_n=5/n', 'EX_n=5', '\\operatorname{Var}(X_n)=5-\\frac{25}{n}', '\\frac52', 'k', 'q_k']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
