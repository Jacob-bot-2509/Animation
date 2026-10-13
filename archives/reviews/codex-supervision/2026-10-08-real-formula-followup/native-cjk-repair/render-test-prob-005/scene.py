from manim import *
FORMULAS = ['X,Y', 'U(0,1)', 'Z=X+Y', 'P(Z>\\frac32)', 'f_Z(z)=\\int_{\\mathbb R}\\mathbf1_{(0,1)}(x)\\mathbf1_{(0,1)}(z-x)\\,dx', 'f_Z(z)=\\begin{cases}z,&0<z<1,\\\\2-z,&1\\le z<2,\\\\0,&\\text{其他}.\\end{cases}', 'P(Z>\\frac32)=\\int_{3/2}^2(2-z)\\,dz=[2z-z^2/2]_{3/2}^2=2-\\frac{15}{8}=\\frac18', 'P(Z>\\frac32)=\\frac18']
class ConceptScene(Scene):
    def construct(self):
        template = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
        template.add_to_preamble(r"\usepackage[UTF8]{ctex}")
        maths = [MathTex(formula, tex_template=template) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
