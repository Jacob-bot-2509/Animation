from manim import *
from fractions import Fraction
from pathlib import Path
from PIL import Image
import re
import json
FORMULAS = ['E_0', 'E_1', 'E_0=1+\\dfrac{1}{2}E_0+\\dfrac{1}{2}E_1', 'E_1=1+\\dfrac{1}{2}\\cdot 0+\\dfrac{1}{2}E_0', 'E_1=1+\\dfrac{E_0}{2}', 'E_0=1+\\dfrac{E_0}{2}+\\dfrac{1}{2}\\left(1+\\dfrac{E_0}{2}\\right)=\\dfrac{3}{2}+\\dfrac{3E_0}{4}', 'E_0=6', '1/4', 'T', 'P(T>2k)\\le(3/4)^k', 'E[T]\\le2\\sum_{k=0}^{\\infty}(3/4)^k=8<\\infty', '6', 'E_0=1+\\dfrac12E_0+\\dfrac12E_1']
RID = 'eval-prob-011-s1'
def rational(value):
    x = Fraction(str(value))
    if x <= 0:
        raise ValueError("Positive finite dimensions required")
    return x

def axis_centers(size, viewport):
    size, viewport = rational(size), rational(viewport)
    count = max(1, -(-size // viewport))
    if count == 1:
        return [Fraction(0)]
    distance = size - viewport
    return [-distance/2 + distance*i/(count-1) for i in range(count)]

def plan_panels(dimensions, width, height, gap=Fraction(1,4), max_rows=6):
    width, height = rational(width), rational(height)
    if not dimensions or type(max_rows) is not int or max_rows < 1 or gap < 0:
        raise ValueError("Nonempty dimensions and positive row limit required")
    dims = [(rational(w), rational(h)) for w,h in dimensions]
    panels, pending = [], []
    def flush():
        if not pending:
            return
        total = sum(dims[i][1] for i in pending) + gap*(len(pending)-1)
        y = total/2
        items=[]
        for i in pending:
            y -= dims[i][1]/2
            items.append({"formula_index":i,"x":Fraction(0),"y":y})
            y -= dims[i][1]/2+gap
        panels.append({"kind":"FULL_FORMULAS","items":items})
        pending.clear()
    for i,(w,h) in enumerate(dims):
        if w>width or h>height:
            flush()
            xs, ys = axis_centers(w,width), axis_centers(h,height)
            if len(xs)*len(ys)>400:
                raise ValueError("Oversized formula requires more than 400 views; never shrink silently")
            for row,cy in enumerate(reversed(ys)):
                for col,cx in enumerate(xs):
                    panels.append({"kind":"FORMULA_SEGMENT","items":[{"formula_index":i,"x":-cx,"y":-cy}],
                                   "tile":[row,col],"tile_grid":[len(ys),len(xs)]})
        else:
            required = sum(dims[j][1] for j in pending)+h+gap*len(pending)
            if pending and (len(pending)>=max_rows or required>height):
                flush()
            pending.append(i)
    flush()
    return panels


class ConceptScene(Scene):
    def construct(self):
        if any(re.search(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]", f) for f in FORMULAS):
            template=TexTemplate(tex_compiler="xelatex", output_format=".xdv")
            template.add_to_preamble(r"\usepackage[UTF8]{ctex}")
            maths=[MathTex(formula, font_size=48, tex_template=template) for formula in FORMULAS]
        else:
            maths=[MathTex(formula, font_size=48) for formula in FORMULAS]
        width=rational(config.frame_width)-1
        height=rational(config.frame_height)-2
        dimensions=[(m.width,m.height) for m in maths]
        panels=plan_panels(dimensions,width,height)
        folder=Path(__file__).parent/"pages"
        results=[]
        for number,panel in enumerate(panels,1):
            self.clear()
            items=[]
            for item in panel["items"]:
                m=maths[item["formula_index"]].copy()
                m.move_to([float(item["x"]),float(item["y"]),0])
                items.append(m)
            self.add(*items)
            # Mask reserved margins. Oversized formulas retain full font size
            # and traverse labelled overlapping views, never global shrink.
            fw,fh=float(config.frame_width),float(config.frame_height)
            masks=VGroup(
                Rectangle(width=fw,height=1,fill_color=BLACK,fill_opacity=1,stroke_width=0).move_to([0,(fh-1)/2,0]),
                Rectangle(width=fw,height=1,fill_color=BLACK,fill_opacity=1,stroke_width=0).move_to([0,-(fh-1)/2,0]),
                Rectangle(width=1/2,height=fh,fill_color=BLACK,fill_opacity=1,stroke_width=0).move_to([(fw-1/2)/2,0,0]),
                Rectangle(width=1/2,height=fh,fill_color=BLACK,fill_opacity=1,stroke_width=0).move_to([-(fw-1/2)/2,0,0]),
            )
            self.add(masks)
            indices=[x["formula_index"]+1 for x in panel["items"]]
            caption=RID+" | page "+str(number)+"/"+str(len(panels))+" | formulas "+",".join(map(str,indices))
            if panel["kind"]=="FORMULA_SEGMENT":
                caption+=" | segment "+str(panel["tile"][0]+1)+","+str(panel["tile"][1]+1)
            label=Text(caption,font_size=20).move_to([0,(fh-1)/2,0])
            if label.width>fw-1:
                label.scale((fw-1)/label.width)
            self.add(label)
            self.wait(3)
            frame=folder/("page-"+str(number).zfill(3)+".png")
            results.append({"page":number,"kind":panel["kind"],"items":[{k:str(v) if k in ("x","y") else v for k,v in i.items()} for i in panel["items"]],
                            "tile":panel.get("tile"),"tile_grid":panel.get("tile_grid"),"frame":frame.name})
        geometry={"schema":"exact-formula-pages-hd-v1","pixel_width":config.pixel_width,"pixel_height":config.pixel_height,"fps":str(config.frame_rate),"page_seconds":"3","id":RID,"font_size":48,"formula_scale":"1",
                  "viewport_width":str(width),"viewport_height":str(height),
                  "dimensions":[[str(rational(w)),str(rational(h))] for w,h in dimensions],
                  "pages":results}
        (Path(__file__).parent/"page-geometry.json").write_text(json.dumps(geometry,indent=2)+"\n",encoding="utf-8")
