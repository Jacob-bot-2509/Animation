from manim import *
from fractions import Fraction
from pathlib import Path
from PIL import Image
import re
import json
FORMULAS = ['p_n\\in[0,1]', 'np_n\\to\\lambda\\in[0,+\\infty)', 'X_n\\sim B(n,p_n)', 'k\\in\\mathbb Z_{\\ge0}', 'P(X_n=k)', '\\lambda', '\\lambda=0', '\\lambda>0', 'np_n\\to\\lambda', 'p_n\\to0', 'k\\ge0', 'n\\ge k', 'P(X_n=k)=\\frac{(np_n)^k}{k!}\\prod_{j=0}^{k-1}(1-\\frac jn)(1-p_n)^n(1-p_n)^{-k}', 'k=0', '1', '0\\le u<1', '-\\frac{u}{1-u}\\le\\log(1-u)\\le-u', '-\\frac{np_n}{1-p_n}\\le n\\log(1-p_n)\\le-np_n', 'n\\log(1-p_n)\\to-\\lambda', '(1-p_n)^n\\to e^{-\\lambda}', '\\lambda^k/k!', 'P(X_n=k)\\to e^{-\\lambda}\\lambda^k/k!', 'P(X_n\\ge1)\\le E X_n=np_n\\to0', 'P(X_n=0)\\to1', 'k\\ge1', 'P(X_n=k)\\to0', '\\displaystyle\\lim_{n\\to\\infty}P(X_n=k)=\\frac{e^{-\\lambda}\\lambda^k}{k!}', '0', 'q_k=e^{-5}5^k/k!', 'n\\in\\mathbb Z,\\ n\\ge5,\\ p_n=5/n', 'n=10', 'p_n=\\frac12', '\\binom nk(5/n)^k(1-5/n)^{n-k}', 'n', 'p_n=5/n', 'EX_n=5', '\\operatorname{Var}(X_n)=5-\\frac{25}{n}', '\\frac52', 'k', 'q_k']
RID = 'prob-040'
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
