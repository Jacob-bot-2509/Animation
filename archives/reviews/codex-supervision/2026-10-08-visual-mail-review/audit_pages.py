"""Independent packet/video/frame/bound source and page-coverage verification."""
from pathlib import Path
from fractions import Fraction as F
import ast,json,hashlib,sys
import av
import numpy as np
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[3]
OWNER=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"tools"))
import core_signatures as core
import native_render_pilot as native
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(condition,message):
    if not condition:raise ValueError(message)
def cover_axis(offsets,size,viewport):
    intervals=sorted({(-F(x)-viewport/2,-F(x)+viewport/2) for x in offsets})
    require(bool(intervals),"No coverage")
    end=intervals[0][1]
    require(intervals[0][0]<=-size/2,"Missing start of formula")
    for lo,hi in intervals[1:]:
        require(lo<=end,"Gap between formula segments")
        end=max(end,hi)
    require(end>=size/2,"Missing end of formula")
def verify_geometry(g,count):
    require(g["font_size"]==48 and F(g["formula_scale"])==1,"Tiny/rescaled formula")
    width,height=F(g["viewport_width"]),F(g["viewport_height"])
    dims=[(F(w),F(h)) for w,h in g["dimensions"]]
    require(len(dims)==count and all(w>0 and h>0 for w,h in dims),"Wrong dimensions")
    require(width>0 and height>0,"Invalid viewport")
    by={i:[] for i in range(count)}
    pages=g["pages"]
    require(pages and [p["page"] for p in pages]==list(range(1,len(pages)+1)),"Missing/duplicate page")
    require(len({p["frame"] for p in pages})==len(pages),"Duplicate frame")
    for p in pages:
        require(p["kind"] in ("FULL_FORMULAS","FORMULA_SEGMENT"),"Unknown page kind")
        require(bool(p["items"]),"Empty page")
        if p["kind"]=="FORMULA_SEGMENT":require(len(p["items"])==1,"Invalid segment")
        for item in p["items"]:
            idx=item["formula_index"];require(type(idx)is int and idx in by,"Unknown formula")
            x,y=F(item["x"]),F(item["y"]);w,h=dims[idx]
            by[idx].append((p["kind"],x,y))
            if p["kind"]=="FULL_FORMULAS":
                require(abs(x)+w/2<=width/2 and abs(y)+h/2<=height/2,"Clipped full formula")
        if p["kind"]=="FULL_FORMULAS":
            rectangles=[(F(i["y"])-dims[i["formula_index"]][1]/2,F(i["y"])+dims[i["formula_index"]][1]/2) for i in p["items"]]
            rectangles.sort()
            require(all(b[0]>=a[1] for a,b in zip(rectangles,rectangles[1:])),"Overlapping formulas")
    for i,occ in by.items():
        require(occ,"Missing formula")
        if any(k=="FULL_FORMULAS" for k,_,_ in occ):
            require(len(occ)==1,"Formula duplicate/mixed coverage")
        else:
            w,h=dims[i]
            xs={x for _,x,_ in occ};ys={y for _,_,y in occ}
            require(len(occ)==len(xs)*len(ys),"Missing/duplicate segment cell")
            require({(x,y) for _,x,y in occ}=={(x,y) for x in xs for y in ys},"Segment grid holes")
            cover_axis(xs,w,width);cover_axis(ys,h,height)
    return len(pages)

def verify_one(result,qualified,binding,correction):
    rid=result["id"]
    work=core.checked_path(ROOT/result["mp4_path"],OWNER).parents[3].parent
    require(work.name=="render-"+rid,"Wrong render folder")
    require(result["rc"]==0 and not result["timed_out"] and result["status"]=="PASS_LOCAL_FORMULA_PAGES","Failed render")
    record=core.load_record({rid:binding},rid)
    for key in ("source_sha256","record_sha256","math_sha256"):
        require(result[key]==binding[key]==qualified[key],"Changed mathematical/source binding")
    formulas,locations=native.formula_inventory(record)
    inventory=work/"formula-inventory.json"
    require(sha(inventory)==result["formula_inventory_sha256"],"Inventory changed")
    require(json.loads(inventory.read_text("utf-8"))=={"unique_formulas":formulas,"source_occurrences":locations},"Dropped/replaced formula")
    source=work/"scene.py"
    require(sha(source)==result["scene_py_sha256"],"Scene changed")
    tree=ast.parse(source.read_text("utf-8"))
    literal=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name)and t.id=="FORMULAS" for t in n.targets))
    require(literal==formulas,"Scene formula strings differ")
    for c in (x for x in ast.walk(tree) if isinstance(x,ast.Call)):
        if isinstance(c.func,ast.Name) and c.func.id=="MathTex":
            require(isinstance(c.args[0],ast.Name) and c.args[0].id=="formula","Wrong MathTex argument")
            require(any(k.arg=="font_size" and isinstance(k.value,ast.Constant) and k.value.value==48 for k in c.keywords),"Wrong font size")
        if isinstance(c.func,ast.Attribute) and c.func.attr=="scale":
            require(isinstance(c.func.value,ast.Name) and c.func.value.id=="label","Rescaled mathematical glyphs")
    geometry=work/"page-geometry.json"
    require(sha(geometry)==result["geometry_sha256"],"Geometry changed")
    g=json.loads(geometry.read_text("utf-8"))
    require(g["id"]==rid,"Geometry identity changed")
    count=verify_geometry(g,len(formulas))
    require(count==result["page_count"]==len(result["frames"]),"Page count mismatch")
    require(correction["id"]==rid and correction["source_mp4_sha256"]==result["mp4_sha256"],"Unbound corrected frames")
    require(correction["geometry_sha256"]==result["geometry_sha256"],"Wrong corrected geometry")
    require(correction["original_render_receipt_sha256"]==sha(work/"receipt.json"),"Raw receipt changed")
    for raw in result["frames"]:
        raw_path=core.checked_path(ROOT/raw["path"],work/"pages")
        require(sha(raw_path)==raw["sha256"],"Original failed screenshot changed")
    bounds={Path(f["path"]).name:f for f in correction["frames"]}
    require(len(bounds)==count,"Duplicate frame bindings")
    images=[]
    for p in g["pages"]:
        require(p["frame"] in bounds,"Missing frame binding")
        f=bounds[p["frame"]]
        path=core.checked_path(ROOT/f["path"],OWNER/"corrected-video-pages"/rid)
        require(sha(path)==f["sha256"],"PNG changed")
        arr=np.array(Image.open(path).convert("RGB"))
        # Exclude caption and margins; an all-black formula area must fail.
        h,w=arr.shape[:2]
        region=arr[h//8:7*h//8,w//28:27*w//28]
        require(np.any(region>32),"No visible formula ink")
        images.append(arr)
    video=core.checked_path(ROOT/result["mp4_path"],work)
    require(sha(video)==result["mp4_sha256"],"Video changed")
    comparisons=[];frames=0
    with av.open(str(video)) as container:
        stream=container.streams.video[0]
        require(F(stream.average_rate)==15,"Unexpected video frame rate")
        for frame in container.decode(stream):
            if frames%45==0:
                page=frames//45
                require(page<count,"Unexpected extra page")
                decoded=np.array(frame.to_image().convert("RGB"))
                require(decoded.shape==images[page].shape,"Wrong video dimensions")
                delta=np.abs(decoded.astype("int16")-images[page].astype("int16"))
                mae=F(int(delta.sum()),int(delta.size))
                require(mae==0,"Corrected PNG must match actual video pixels exactly")
                require(F(frame.pts)*F(frame.time_base)==page*3,"Wrong page timing")
                comparisons.append(str(mae))
            frames+=1
    require(frames==count*45 and len(comparisons)==count,"Missing video pages")
    return {"id":rid,"status":"PASS_BOUND_EXACT_FORMULA_PAGES","formula_count":len(formulas),
            "source_formula_occurrences":len(locations),"page_count":count,"font_size":48,"formula_scale":"1",
            "full_pages":sum(p["kind"]=="FULL_FORMULAS" for p in g["pages"]),
            "segment_pages":sum(p["kind"]=="FORMULA_SEGMENT" for p in g["pages"]),
            "video_frames":frames,"page_video_mae_exact":comparisons,
            "record_sha256":binding["record_sha256"],"math_sha256":binding["math_sha256"],
            "mp4_path":result["mp4_path"],"mp4_sha256":result["mp4_sha256"],
            "visual_glyph_review":"SEPARATE_IMAGE_REVIEW_REQUIRED","production":"CLOSED"}
def main():
    frozen=ROOT/"reviews/codex-supervision/2026-10-08-real-formula-followup"
    old=[json.loads(l) for l in (frozen/"qualified-records.jsonl").read_text("utf-8").splitlines()]
    by={r["id"]:r for r in old}
    bindings={r["id"]:r for r in core.load_record_bindings()}
    results=[]
    for i in range(1,4):
        shard=OWNER/("shard-"+str(i))
        receipt=json.loads((shard/"receipt.json").read_text("utf-8"))
        require(receipt["summary"]=={"total":55,"passed":55,"failed":0},"Failed/incomplete shard")
        results.extend(receipt["results"])
    require(len(results)==165 and len({r["id"] for r in results})==165 and {r["id"] for r in results}==set(by),"Not full 165-record coverage")
    corrections={r["id"]:r for r in (json.loads(l) for l in (OWNER/"corrected-frames.jsonl").read_text("utf-8").splitlines())}
    require(set(corrections)==set(by),"Incomplete corrected exports")
    audits=[]
    for result in results:
        audit=verify_one(result,by[result["id"]],bindings[result["id"]],corrections[result["id"]]);audits.append(audit)
        if len(audits)%15==0:print("Independent page/video checks",len(audits),flush=True)
    (OWNER/"qualified-readable-pages.jsonl").write_bytes(b"".join((json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n").encode("utf-8") for r in audits))
    summary={"records":len(audits),"unique_formula_items":sum(r["formula_count"] for r in audits),
             "source_formula_occurrences":sum(r["source_formula_occurrences"] for r in audits),
             "pages":sum(r["page_count"] for r in audits),"segment_pages":sum(r["segment_pages"] for r in audits),
             "status":"PASS_BOUND_EXACT_FORMULA_PAGE_LAYOUT_AND_VIDEO_CONTENT",
             "all_record_math_and_scene_text":"UNCHANGED","full_glyph_level_visual_acceptance":"NOT_ESTABLISHED",
             "native_sandbox":"UNVERIFIED","semantic_isolation":"NOT_ESTABLISHED","production":"CLOSED","PASS_CORE_SCOPE_issued":False}
    (OWNER/"independent-page-summary.json").write_bytes(core.encoded(summary))
    print(json.dumps(summary),flush=True)
if __name__=="__main__":main()
