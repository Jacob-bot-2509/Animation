from manim import *
FORMULAS = ['b_1,b_2,b_3\\in\\mathbb Z', '\\begin{cases}x+y+z=b_1\\\\x-y+z=b_2\\\\x+y-z=b_3\\end{cases}', '(x,y,z)\\in\\mathbb Z^3', 'A=\\begin{pmatrix}1&1&1\\\\1&-1&1\\\\1&1&-1\\end{pmatrix}', 'D=\\det A=4\\ne0', '\\mathbb Q^3', 'D_x=2(b_2+b_3)', 'D_y=2(b_1-b_2)', 'D_z=2(b_1-b_3)', 'x=\\frac{b_2+b_3}{2}', 'y=\\frac{b_1-b_2}{2}', 'z=\\frac{b_1-b_3}{2}', 'x,y,z\\in\\mathbb Z', 'b_1-b_2=2y', 'b_1-b_3=2z', 'b_1\\equiv b_2\\equiv b_3\\pmod2', 'b_1,b_2,b_3', '\\det A\\ne0', 'A\\mathbb Z^3=\\{b\\in\\mathbb Z^3:b_1\\equiv b_2\\equiv b_3\\pmod2\\}', '(b_1-b_2,b_1-b_3)\\bmod2', '4', '\\mathbb Z^3', '(x,y,z)=\\left(\\frac{b_2+b_3}{2},\\frac{b_1-b_2}{2},\\frac{b_1-b_3}{2}\\right)', 'b\\in\\mathbb Z^3', '\\det A=4', '\\frac{b_2+b_3}{2},\\frac{b_1-b_2}{2},\\frac{b_1-b_3}{2}', 'A\\mathbb Z^3', 'D=4', 'D_x,D_y,D_z', 'D\\ne0']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
