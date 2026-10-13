from manim import *
FORMULAS = ['4x^2-y^2+z^2=1', 's', '\\begin{cases}x=\\dfrac{\\cos\\theta+s\\sin\\theta}{2}\\\\y=s\\\\z=\\sin\\theta-s\\cos\\theta\\end{cases}', '\\begin{cases}x=\\dfrac{\\cos\\theta-s\\sin\\theta}{2}\\\\y=s\\\\z=\\sin\\theta+s\\cos\\theta\\end{cases}', '4x^2+z^2-y^2=(\\cos\\theta\\pm s\\sin\\theta)^2+(\\sin\\theta\\mp s\\cos\\theta)^2-s^2=\\cos^2\\theta+\\sin^2\\theta\\pm 2s\\sin\\theta\\cos\\theta\\mp 2s\\sin\\theta\\cos\\theta+s^2(\\sin^2\\theta+\\cos^2\\theta)-s^2=1', 'y=k', '4x^2+z^2=1+k^2', 'z=k', '4x^2-y^2=1-k^2', '|k|<1', 'x', '|k|>1', 'y', '|k|=1', 'y=\\pm2x', 'x=k', 'z^2-y^2=1-4k^2', '|k|<1/2', 'z', '|k|>1/2', '|k|=1/2', 'z=\\pm y', 'k=\\pm1', 'k=\\pm1/2']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
