from manim import *
FORMULAS = ['a\\in\\mathbb R', 'f(x,y,z)=x^2+2y^2+az^2+2xy+2xz', 'a', 'f', 'A', 'LDL^T', 'A=L\\operatorname{diag}(1,1,a-2)L^T,\\qquad L=\\begin{pmatrix}1&0&0\\\\1&1&0\\\\1&-1&1\\end{pmatrix}.', '1,2,0', '1,0,a', 'L', '(u,v,w)^T=L^T(x,y,z)^T', 'u=x+y+z,\\ v=y-z,\\ w=z', 'f=(x,y,z)A(x,y,z)^T=(L^T(x,y,z)^T)^T\\operatorname{diag}(1,1,a-2)(L^T(x,y,z)^T)=u^2+v^2+(a-2)w^2,', 'u^2+v^2+(a-2)w^2', '\\Delta_1=1,\\Delta_2=1,\\Delta_3=|A|=a-2', '\\iff\\Delta_3>0\\iff a>2', 'a=2', 'f=u^2+v^2', 'u=v=0', 'x+y+z=0,\\ y=z', 't(-2,1,1)', 'f=(x+y+z)^2+(y-z)^2+(a-2)z^2', 'a>2', '\\Delta_3=a-2']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
