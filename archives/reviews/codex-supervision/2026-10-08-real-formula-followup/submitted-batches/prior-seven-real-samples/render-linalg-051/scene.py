from manim import *
FORMULAS = ['\\mathbb R[x]', '\\Delta p(x)=p(x+1)-p(x)', '\\ker\\Delta', '\\Delta:\\mathbb R[x]\\to\\mathbb R[x]', '\\Delta p(x)=3x^2+3x+1', 'p(0)=0', '\\Delta', 'p(x)=a_nx^n+\\cdots', 'n\\ge1', 'a_n\\ne0', '\\Delta p(x)=na_nx^{n-1}+\\cdots\\ne0', '\\ker\\Delta=\\mathbb R\\cdot1', 'g', 'm\\ge0', 'c_mx^m', '\\Delta(\\frac{c_m}{m+1}x^{m+1})', 'm', 'c', 'cx', '(x+1)^3-x^3=3x^2+3x+1', 'x^3', 'p=x^3+C', 'C=0', '\\operatorname{im}\\Delta=\\mathbb R[x]', 'p(x)=x^3', 'p(x)\\mapsto p(x+1)-p(x)', 'a_nx^n\\mapsto na_nx^{n-1}', '\\frac{c_m}{m+1}x^{m+1}', 'x^3+C']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
