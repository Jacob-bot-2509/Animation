"""Reviewed record-specific scenes. Unknown rows are refused, not generic clones."""
from __future__ import annotations
SCENE_SOURCE = r"""
from manim import *
class ConceptScene(Scene):
    def construct(self):
        formula=MathTex(r'f(x)=x^2,\quad x=1',color=WHITE)
        derivative=MathTex(r"f'(x)=2x",color=WHITE)
        answer=MathTex(r'y=2x-1',color=WHITE)
        point_label=MathTex(r'(1,1)',color=BLACK)
        title=Text('求函数在指定点处的切线方程',font='Microsoft YaHei',font_size=28,color=WHITE)
        title.to_edge(UP);formula.scale(3/4).next_to(title,DOWN)
        panel=Rectangle(width=9,height=4.2,fill_color=GRAY_A,fill_opacity=1,stroke_width=0).shift(DOWN/5)
        axes=Axes(x_range=[-2,3,1],y_range=[-2,6,2],x_length=7,y_length=3.4,
                  axis_config={'color':BLACK,'include_numbers':True,'font_size':18,
                               'decimal_number_config':{'color':BLACK,'num_decimal_places':0}}).move_to(panel)
        curve=axes.plot(lambda x:x*x,x_range=[-2,12/5,1/100],color=BLUE)
        dot=Dot(axes.c2p(1,1),color=YELLOW,radius=1/10,stroke_color=BLACK,stroke_width=2)
        point_label.scale(1/2).next_to(dot,UR)
        tangent=axes.plot(lambda x:2*x-1,x_range=[-1/2,3,1/100],color=ORANGE)
        derivative.scale(3/4).move_to(LEFT*3+DOWN*3)
        answer.scale(3/4).move_to(RIGHT*3+DOWN*3)
        self.add(title,formula,panel)
        self.play(Create(axes),run_time=1/2)
        self.play(Create(curve),run_time=1/2)
        self.play(FadeIn(dot),Write(point_label),run_time=1/2)
        self.play(Indicate(dot,color=YELLOW),run_time=1/2)
        self.play(Create(tangent),run_time=1/2)
        self.play(Write(derivative),run_time=1/2)
        self.play(Write(answer),run_time=1/2)
        self.wait(1/2)
"""
INPUT_SHA256='0f6fb3cbd0c062c313954b405d9c39478ccfb4935413b48bc1b78626e1545dd0'


def build_scene(record, input_sha256):
    if record.get('id')!='calc-derivative-001' or input_sha256!=INPUT_SHA256:
        raise ValueError('No reviewed record-specific renderer for this row')
    return SCENE_SOURCE
