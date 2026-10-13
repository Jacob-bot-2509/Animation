from manim import *
import numpy as np
class ConceptScene(Scene):
    def construct(self):
        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)
        maths = [MathTex(r'') for r in [
            'A',
            '\\dfrac{d}{dt}e^{tA}=Ae^{tA}',
            'e^{tA}=\\displaystyle\\sum_{k=0}^{\\infty}\\dfrac{t^kA^k}{k!}',
            't',
            '\\dfrac{d}{dt}e^{tA}=\\displaystyle\\sum_{k=1}^{\\infty}\\dfrac{kt^{k-1}A^k}{k!}=\\sum_{k=1}^{\\infty}\\dfrac{t^{k-1}A^k}{(k-1)!}=A\\sum_{m=0}^{\\infty}\\dfrac{t^mA^m}{m!}=Ae^{tA}',
            "X'=AX",
            'X(0)=I',
            'R>0',
            '|t|\\le R',
            'R^k\\|A\\|^k/k!',
            'R^{k-1}\\|A\\|^k/(k-1)!',
            'k\\ge1',
            'e^{R\\|A\\|}',
            '\\|A\\|e^{R\\|A\\|}',
        ]]
        group = VGroup(*maths)
        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)
        self.add(group)
        label = Text('trusted-sample-render', font_size=24).to_corner(UL)
        self.add(label)
        self.wait(0.2)
