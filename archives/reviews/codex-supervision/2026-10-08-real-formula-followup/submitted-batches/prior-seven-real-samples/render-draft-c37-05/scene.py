from manim import *
FORMULAS = ['V', 'S,T\\in\\operatorname{End}(V)', 'ST-TS=I_V', '\\mathbb R[x]', 'n=\\dim V\\ge1', 'S,T', '(s_{ij}),(t_{ij})', '\\operatorname{tr}(ST)=\\sum_{i,j}s_{ij}t_{ji}=\\sum_{i,j}t_{ij}s_{ji}=\\operatorname{tr}(TS)', '0=\\operatorname{tr}(ST-TS)=\\operatorname{tr}I_V=n', 'n\\ge1', "D(p)=p'", 'M(p)=xp', "(DM-MD)(p)=(xp)'-xp'=p", 'DM-MD=I', '\\operatorname{tr}(ST)=\\operatorname{tr}(TS)', '0=\\operatorname{tr}(ST-TS)=\\operatorname{tr}I_V=n\\ne0', '(DM-MD)(p)=p']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
