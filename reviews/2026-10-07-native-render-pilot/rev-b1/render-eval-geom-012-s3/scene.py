from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'x=a\\cos t,\\ y=a\\sin t,\\ z=bt',
            'a,b>0',
            '\\alpha',
            '\\tan\\alpha=\\dfrac{b}{a}',
            '2\\pi b',
            '2\\pi a',
            '\\cos^2\\alpha=\\dfrac{a^2}{a^2+b^2}',
            '\\kappa=\\dfrac{\\cos^2\\alpha}{a}=\\dfrac{a}{a^2+b^2}',
            '\\tau=\\dfrac{\\sin\\alpha\\cos\\alpha}{a}=\\dfrac{b}{a^2+b^2}',
            '\\dfrac{\\tau}{\\kappa}=\\dfrac{b}{a}',
            'e_r=(\\cos t,\\sin t,0)',
            'e_\\theta=(-\\sin t,\\cos t,0)',
            'e_z=(0,0,1)',
            '\\tan\\alpha=b/a',
            'T=\\cos\\alpha\\,e_\\theta+\\sin\\alpha\\,e_z',
            'ds/dt=a/\\cos\\alpha',
            'dT/ds=-(\\cos^2\\alpha/a)e_r',
            'N=-e_r',
            '\\kappa=\\cos^2\\alpha/a',
            'B=T\\times N=\\cos\\alpha\\,e_z-\\sin\\alpha\\,e_\\theta',
            'dB/ds=(\\sin\\alpha\\cos\\alpha/a)e_r=-\\tau N',
            '\\tau=\\sin\\alpha\\cos\\alpha/a',
            '\\cos\\alpha=a/\\sqrt{a^2+b^2}',
            '\\sin\\alpha=b/\\sqrt{a^2+b^2}',
            '\\kappa=a/(a^2+b^2)',
            '\\tau=b/(a^2+b^2)',
            '\\kappa=\\dfrac{a}{a^2+b^2}',
            '\\tau=\\dfrac{b}{a^2+b^2}',
            '\\kappa:\\tau=a:b',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
