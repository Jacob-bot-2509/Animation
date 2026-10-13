from manim import *
FORMULAS = ['\\mathbb{R}^2', '\\omega(u,v)=u_1v_2-u_2v_1', 'J=\\begin{pmatrix}0&1\\\\-1&0\\end{pmatrix}', '\\omega(u,v)=u^TJv=\\det(u,v)', 'A=\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}', 'A^TJA=\\begin{pmatrix}0&ad-bc\\\\bc-ad&0\\end{pmatrix}=(\\det A)J', '\\omega(Au,Av)=(\\det A)\\omega(u,v)', 'A', '\\det A=1', 'R=\\operatorname{diag}(1,-1)', '-1', '\\omega(Ru,Rv)=-\\omega(u,v)', '\\omega(Au,Av)=\\omega(u,v)', 'A^TJA=(\\det A)J']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
