from manim import *
FORMULAS = ['f(x,y)=x^2+2xy+ay^2', '1', 'a', 'a=0', 'a=1', 'a=2', 'u=x+y,v=y', 'f=u^2+(a-1)v^2', 'C=\\begin{pmatrix}1&-1\\\\0&1\\end{pmatrix}', 'C^{\\mathsf T}AC=\\operatorname{diag}(1,a-1)', '\\det C=1', 'A_{11}=1\\ne0', '\\operatorname{rank}A\\ge1', '\\det A=a-1', 'u^2-v^2', '(1,1,0)', '2', 'u^2+0v^2', '(1,0,1)', 'u^2+v^2', '(2,0,0)', 'a=1\\iff\\operatorname{rank}A=1', 'a=0,1,2', 'u^2-v^2,u^2+0v^2,u^2+v^2', '(n_+,n_-,n_0)', '(1,1,0),(1,0,1),(2,0,0)', 'f=x^2+2xy+ay^2', 'A=\\begin{pmatrix}1&1\\\\1&a\\end{pmatrix}', '(x+y)^2-y^2', '(x+y)^2', '(x+y)^2+y^2']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
