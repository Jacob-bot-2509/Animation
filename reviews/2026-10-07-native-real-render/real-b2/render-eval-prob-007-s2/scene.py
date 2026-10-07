from manim import *
FORMULAS = ['q_k', 'k', 'q_1=1', 'k-1', 'q_k=q_{k-1}\\frac{366-k}{365}', 'q_{30}=\\prod_{k=2}^{30}\\frac{366-k}{365}=\\frac{365!}{335!\\,365^{30}}', '1-q_{30}', '1-\\frac{365!}{335!\\,365^{30}}', '366-k', 'q_k=q_{k-1}(366-k)/365', 'q_{30}=\\prod_{k=2}^{30}(366-k)/365=365!/(335!\\,365^{30})']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
