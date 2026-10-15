from manim import *
FORMULAS = ['\\sum_{n=1}^{\\infty} \\frac{(-1)^n}{\\sqrt{n}}', 'u_n=1/\\sqrt n', 'u_{n+1}\\le u_n', '\\lim_{n\\to\\infty}u_n=0', '\\sum_{n=1}^{\\infty}(-1)^n u_n', 'S', 'N', 'S_N', '|S-S_N|\\le 1/\\sqrt{N+1}', '\\sum_{n=1}^{N}1/\\sqrt n\\ge\\int_1^{N+1}x^{-1/2}\\,dx=2(\\sqrt{N+1}-1)\\to+\\infty', 'p=\\frac{1}{2}\\le1', 'p', 'u_n\\downarrow0', '|S-S_N|\\le1/\\sqrt{N+1}', '\\sum_{n=1}^Nn^{-1/2}\\ge\\int_1^{N+1}x^{-1/2}\\,dx=2(\\sqrt{N+1}-1)\\to+\\infty']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
