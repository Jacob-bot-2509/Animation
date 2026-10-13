from manim import *
FORMULAS = ['z = x^2 + y^2', '(x_0, y_0, z_0)', '(l, m, n)', '(x_0+lt, y_0+mt, z_0+nt)', 'z=x^2+y^2', 't^2(l^2+m^2)+t(2x_0l+2y_0m-n)+(x_0^2+y_0^2-z_0)=0', 't', 'l^2+m^2=0', 'l=m=0', '2x_0l+2y_0m-n=0', 'n=0', '(x,y,z)=(x_0+lt,y_0+mt,z_0+nt)', '(l,m,n)\\ne(0,0,0)', 't\\in\\mathbb R', '-n=0', '(l,m,n)=(0,0,0)']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
