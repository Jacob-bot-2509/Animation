from manim import *
FORMULAS = ['\\mathbb R^3', '\\pi_1=\\{(x,y,z):x=0\\}', '\\pi_2=\\{(x,y,z):x+y=0\\}', '\\Pi_1,\\Pi_2', 'P_0=(a,b,c)', 'a,b,c\\in\\mathbb R', 'P_{n+1}=\\Pi_1\\Pi_2P_n', '\\pi_2', '\\pi_1', 'P_n', '\\Pi_1\\Pi_2', '\\Pi_1(x,y,z)=(0,y,z)', '(1,1,0)', '\\Pi_2(x,y,z)=(x,y,z)-\\frac{x+y}{2}(1,1,0)=((x-y)/2,(y-x)/2,z)', 'B_1=\\operatorname{diag}(0,1,1)', 'B_2=\\begin{pmatrix}1/2&-1/2&0\\\\-1/2&1/2&0\\\\0&0&1\\end{pmatrix}', '\\pi_1,\\pi_2', 'A=B_1B_2=\\begin{pmatrix}0&0&0\\\\-1/2&1/2&0\\\\0&0&1\\end{pmatrix}', 'P_1=(0,(b-a)/2,c)', 'n\\ge1', 'A^n=\\begin{pmatrix}0&0&0\\\\-1/2^n&1/2^n&0\\\\0&0&1\\end{pmatrix}', 'P_n=(0,(b-a)/2^n,c)', 'n=0', 'P_0', 'P_n\\to Q=(0,0,c)', 'Q', '\\pi_1\\cap\\pi_2=\\{(0,0,z):z\\in\\mathbb R\\}', '\\|P_0-Q\\|=\\sqrt{a^2+b^2}', '\\|P_n-Q\\|=|b-a|/2^n', 'a=b=0', 'a=b\\ne0', 'a\\ne b', '|b-a|/2^n>0', 'Ae_2=e_2/2', 'A^2e_2=e_2/4', 'A^2\\ne A', '\\Pi_1=B_1=\\operatorname{diag}(0,1,1)', '\\Pi_2=B_2=\\begin{pmatrix}1/2&-1/2&0\\\\-1/2&1/2&0\\\\0&0&1\\end{pmatrix}', 'Q=(0,0,c)', '\\sqrt{a^2+b^2}', '|b-a|/2^n', 'x=0', 'x+y=0', 'x=y=0', '\\Pi_2P_n', 'P_{n+1}', '\\Pi_2', '\\Pi_1', 'A=B_1B_2']
class ConceptScene(Scene):
    def construct(self):
        maths = [MathTex(formula) for formula in FORMULAS]
        group = VGroup(*maths).arrange(DOWN, buff=1/4)
        group.scale(min((config.frame_width-1)/group.width, (config.frame_height-1)/group.height))
        self.add(group)
        self.wait(1/5)
