from manim import *
FORMULAS = ['f=3x^2+4xy+6y^2', 'f=3\\left(x^2+\\dfrac{4}{3}xy\\right)+6y^2=3\\left(x+\\dfrac{2}{3}y\\right)^2-\\dfrac{4}{3}y^2+6y^2=3\\left(x+\\dfrac{2}{3}y\\right)^2+\\dfrac{14}{3}y^2', 'u=x+\\dfrac{2}{3}y', 'v=y', 'x=u-\\dfrac{2}{3}v', 'y=v', '3u^2+\\dfrac{14}{3}v^2', 'A=\\begin{pmatrix}3&2\\\\2&6\\end{pmatrix}', 'C=\\begin{pmatrix}1&-\\frac{2}{3}\\\\0&1\\end{pmatrix}', 'C^TAC=\\begin{pmatrix}3&0\\\\0&\\frac{14}{3}\\end{pmatrix}', 'AC=\\begin{pmatrix}3&0\\\\2&\\frac{14}{3}\\end{pmatrix}', 'C^T(AC)=\\begin{pmatrix}3&0\\\\0&\\frac{14}{3}\\end{pmatrix}', '\\begin{cases}u=x+\\frac{2}{3}y\\\\v=y\\end{cases}']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
