"""Version-bound readable pages; preserve exact formulas and avoid whole-group shrink."""
from __future__ import annotations
import argparse
from fractions import Fraction
import inspect
import json
from pathlib import Path
import re
import subprocess
import sys
import time
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
import core_signatures as core
import native_render_pilot as native

FONT_SIZE = 48

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

SCENE_BODY = r'''
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
        geometry={"schema":"exact-formula-pages-v1","id":RID,"font_size":48,"formula_scale":"1",
                  "viewport_width":str(width),"viewport_height":str(height),
                  "dimensions":[[str(rational(w)),str(rational(h))] for w,h in dimensions],
                  "pages":results}
        (Path(__file__).parent/"page-geometry.json").write_text(json.dumps(geometry,indent=2)+"\n",encoding="utf-8")
'''

def scene_source(formulas, rid):
    if not formulas or any(not isinstance(f,str) or not f for f in formulas):
        raise ValueError("Nonempty exact formulas required")
    if not native.ID_RE.fullmatch(rid):
        raise ValueError("Invalid record ID")
    return ("from manim import *\nfrom fractions import Fraction\nfrom pathlib import Path\n"
            "from PIL import Image\nimport re\nimport json\n"
            "FORMULAS = "+repr(formulas)+"\nRID = "+repr(rid)+"\n"
            +inspect.getsource(rational)+"\n"+inspect.getsource(axis_centers)+"\n"
            +inspect.getsource(plan_panels)+"\n"+SCENE_BODY)

def decode_pages(video, folder, expected):
    """Extract actual encoded video pages; stale camera screenshots cannot qualify."""
    import av
    if type(expected) is not int or expected<=0:
        raise ValueError("Positive expected page count required")
    folder.mkdir(exist_ok=False)
    total=0
    with av.open(str(video)) as container:
        stream=container.streams.video[0]
        if Fraction(stream.average_rate)!=15:
            raise ValueError("Unexpected frame rate")
        for frame in container.decode(stream):
            if total%45==0:
                page=total//45
                if page>=expected or Fraction(frame.pts)*Fraction(frame.time_base)!=page*3:
                    raise ValueError("Unexpected encoded page timing")
                frame.to_image().save(folder/("page-"+str(page+1).zfill(3)+".png"))
            total+=1
    if total!=45*expected:
        raise ValueError("Missing/extra encoded pages")

def render(rid, work, record, binding, old):
    work.mkdir(exist_ok=False)
    formulas,locations=native.formula_inventory(record)
    scene=work/"scene.py"
    scene.write_text(scene_source(formulas,rid),encoding="utf-8",newline="\n")
    (work/"formula-inventory.json").write_bytes(core.encoded({"unique_formulas":formulas,"source_occurrences":locations}))
    # Bind the old video, but compile new glyphs without reusing unbound SVG caches.
    old_video=core.checked_path(core.ROOT/old["mp4_path"],core.ROOT/"reviews")
    if core.digest(old_video.read_bytes())!=old["mp4_sha256"]:
        raise ValueError("Original qualified video changed")
    command=[str(native.PY),"-B","-m","manim","render",str(scene),"ConceptScene","-ql",
             "--media_dir",str(work/"media"),"--disable_caching"]
    start=time.monotonic_ns()
    try:
        result=subprocess.run(command,capture_output=True,cwd=str(work),timeout=360)
        rc,out,err,timeout=result.returncode,result.stdout,result.stderr,False
    except subprocess.TimeoutExpired as exc:
        rc,out,err,timeout=-1,native.as_bytes(exc.stdout),native.as_bytes(exc.stderr),True
    (work/"stdout.bin").write_bytes(out);(work/"stderr.bin").write_bytes(err)
    videos=list((work/"media").rglob("ConceptScene.mp4"))
    export_ok=False
    if rc==0 and not timeout and len(videos)==1 and (work/"page-geometry.json").exists():
        try:
            geometry=json.loads((work/"page-geometry.json").read_text("utf-8"))
            decode_pages(videos[0],work/"pages",len(geometry["pages"]))
            export_ok=True
        except (ValueError,OSError,KeyError,IndexError) as exc:
            (work/"export-error.json").write_text(json.dumps({"error":str(exc)})+"\n","utf-8")
    frames=list((work/"pages").glob("page-*.png")) if (work/"pages").exists() else []
    ok=rc==0 and not timeout and export_ok and len(videos)==1 and bool(frames) and (work/"page-geometry.json").is_file()
    receipt={"id":rid,"status":"PASS_LOCAL_FORMULA_PAGES" if ok else "FAIL_LOCAL_FORMULA_PAGES",
             "rc":rc,"timed_out":timeout,"elapsed_seconds_exact":str(Fraction(time.monotonic_ns()-start,1000000000)),
             "record_sha256":binding["record_sha256"],"math_sha256":binding["math_sha256"],
             "source_sha256":binding["source_sha256"],"core_manifest_sha256":core.CORE_MANIFEST_SHA256,
             "scene_py_sha256":core.digest(scene.read_bytes()),"unique_formulas":len(formulas),
             "source_formula_occurrences":len(locations),"formula_inventory_sha256":core.digest((work/"formula-inventory.json").read_bytes()),
             "font_size":48,"formula_scale":"1","page_count":len(frames),"page_capture":"DECODED_ACTUAL_VIDEO",
             "mp4_path":videos[0].relative_to(core.ROOT).as_posix() if len(videos)==1 else None,
             "mp4_sha256":core.digest(videos[0].read_bytes()) if len(videos)==1 else None,
             "geometry_sha256":core.digest((work/"page-geometry.json").read_bytes()) if (work/"page-geometry.json").exists() else None,
             "frames":[{"path":p.relative_to(core.ROOT).as_posix(),"sha256":core.digest(p.read_bytes())} for p in sorted(frames)],
             "visual_acceptance":"REQUIRES_BOUND_IMAGE_REVIEW","scope":"TRUSTED_LOCAL_FORMULA_PAGES_ONLY",
             "native_sandbox":"UNVERIFIED","semantic_isolation":"NOT_ESTABLISHED","production":"CLOSED"}
    (work/"receipt.json").write_bytes(core.encoded(receipt))
    return receipt

def run(qualified,ids,out):
    qualified=core.checked_path(qualified,core.ROOT/"reviews")
    raw=qualified.read_bytes()
    old_rows=[json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]
    old={r["id"]:r for r in old_rows}
    if len(old)!=len(old_rows):raise ValueError("Duplicate qualified IDs")
    ids=ids or list(old)
    if not ids or len(ids)!=len(set(ids)):raise ValueError("Unique nonempty IDs required")
    by_id={r["id"]:r for r in core.load_record_bindings()}
    for rid in ids:
        if rid not in old or rid not in by_id:raise ValueError("ID absent from qualified current core")
        record=core.load_record(by_id,rid)
        for field in ("record_sha256","math_sha256","source_sha256"):
            if old[rid][field]!=by_id[rid][field]:raise ValueError("Qualified record binding mismatch")
        formulas,_=native.formula_inventory(record)
        if len(formulas)!=old[rid]["unique_formulas"]:raise ValueError("Formula count mismatch")
    tool=Path(__file__)
    inputs={"schema":"readable-formula-inputs-v1","ids":ids,"qualified_sha256":core.digest(raw),
            "generator_sha256":core.digest(tool.read_bytes()),"native_inventory_tool_sha256":core.digest(Path(native.__file__).read_bytes()),
            "core_tool_sha256":core.digest(Path(core.__file__).read_bytes()),"core_manifest_sha256":core.CORE_MANIFEST_SHA256,
            "bindings":[by_id[rid] for rid in ids]}
    core.publish(out,{"run-inputs.json":core.encoded(inputs),"generator-snapshot.py":tool.read_bytes(),"qualified-input.jsonl":raw})
    results=[]
    for rid in ids:
        row=render(rid,out/("render-"+rid),core.load_record(by_id,rid),by_id[rid],old[rid])
        results.append(row)
        print(json.dumps({k:row[k] for k in ("id","status","rc","page_count")}),flush=True)
    summary={"total":len(results),"passed":sum(r["status"]=="PASS_LOCAL_FORMULA_PAGES" for r in results)}
    summary["failed"]=summary["total"]-summary["passed"]
    with (out/"receipt.json").open("xb") as f:
        f.write(core.encoded({"schema":"readable-formula-receipt-v1","results":results,"summary":summary,
                             "visual_acceptance":"REQUIRES_BOUND_IMAGE_REVIEW","production":"CLOSED"}))
    return 0 if summary["failed"]==0 else 3

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--qualified",type=Path,required=True)
    ap.add_argument("--ids",nargs="+")
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args(argv)
    try:
        return run(a.qualified,a.ids,a.out.absolute())
    except (ValueError,KeyError,TypeError,OSError) as e:
        print(json.dumps({"status":"FAIL_BOUND_PAGE_INPUT","error":str(e),"production":"CLOSED"}))
        return 2
if __name__=="__main__":raise SystemExit(main())
