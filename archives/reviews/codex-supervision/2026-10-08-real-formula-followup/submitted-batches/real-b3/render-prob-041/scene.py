from manim import *
FORMULAS = ['\\mu\\in\\mathbb R', '\\sigma>0', 'X\\sim N(\\mu,\\sigma^2)', '\\mu', '\\sigma', '[\\mu-c\\sigma,\\mu+c\\sigma]', 'c\\ge0', 'f_{\\mu,\\sigma}(x)=\\frac{1}{\\sigma\\sqrt{2\\pi}}\\exp(-\\frac{(x-\\mu)^2}{2\\sigma^2})', '\\phi(z)=\\frac{1}{\\sqrt{2\\pi}}e^{-z^2/2}', 'f_{\\mu,\\sigma}(x)=\\sigma^{-1}\\phi((x-\\mu)/\\sigma)', 'x=\\mu', 'f_{\\mu,\\sigma}(\\mu)=1/(\\sigma\\sqrt{2\\pi})', '1', 'Z=(X-\\mu)/\\sigma\\sim N(0,1)', 'P(|X-\\mu|\\le c\\sigma)=\\frac{1}{\\sqrt{2\\pi}}\\int_{-c}^{c}e^{-z^2/2}\\,dz=\\operatorname{erf}(c/\\sqrt2)', '\\operatorname{erf}(u)=\\frac2{\\sqrt\\pi}\\int_0^u e^{-t^2}\\,dt', 'c=1,2', '\\operatorname{erf}(1/\\sqrt2)', '\\operatorname{erf}(\\sqrt2)', '\\frac1{\\sigma\\sqrt{2\\pi}}', 'P(|X-\\mu|\\le c\\sigma)=\\operatorname{erf}(c/\\sqrt2)', 'f_{\\mu,\\sigma}(x)', '\\mu\\in\\mathbb R,\\ \\sigma>0', 'N(0,1)', '\\int_{\\mathbb R}\\phi(z)\\,dz=1', '[\\mu-\\sigma,\\mu+\\sigma]', '[\\mu-2\\sigma,\\mu+2\\sigma]', 'z=(x-\\mu)/\\sigma']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
