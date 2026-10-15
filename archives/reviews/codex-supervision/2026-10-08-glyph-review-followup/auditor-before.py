"""Independent native-4K/source/page/pixel checks; no global glyph certificate."""
from pathlib import Path
from fractions import Fraction as F
import ast,json,hashlib,sys,importlib.util
import av,numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[3];OWNER=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"tools"))
import core_signatures as core
import native_render_pilot as native
PARENT=ROOT/"reviews/codex-supervision/2026-10-08-visual-mail-review"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(x,msg):
    if not x:raise ValueError(msg)
spec=importlib.util.spec_from_file_location("prior_geometry_auditor",PARENT/"audit_pages.py")
require(sha(PARENT/"audit_pages.py")=="45344de20d1d569111115fcaf280cb41239b04288bc47d7ff7d28f3a7918e45d","Frozen geometry verifier changed")
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
def page_density(path,items):
    require(type(items)is int and items>0,"Wrong per-page item count")
    with Image.open(path) as img:
        require(img.size==(3840,2160),"Wrong actual PNG resolution")
        arr=np.array(img.convert("RGB"))
    # Formula viewport only: x margins half scene-unit and y margins one.
    # Exact inner inclusive pixel bounds conservatively exclude the mask edges.
    region=arr[271:1889,136:3704]
    mask=np.any(region>32,axis=2);yy,xx=np.nonzero(mask)
    require(len(xx)>0,"Empty formula viewport")
    w=int(xx.max()-xx.min()+1);h=int(yy.max()-yy.min()+1)
    return {"displayed_formula_items":items,"ink_pixels":int(len(xx)),
            "bbox_width":w,"bbox_height":h,"bbox_height_per_displayed_item_px_exact":str(F(h,items)),
            "slot_proxy_at_1080p_exact":str(F(h,2*items)),
            "metric_scope":"OCCUPIED_BBOX_SLOT_PROXY_NOT_MINIMUM_GLYPH_SIZE"}
def verify_one(r,parent,binding):
    rid=r["id"];require(r["status"]=="PASS_BOUND_HD_RENDER" and r["rc"]==0 and not r["timed_out"],"Failed render")
    work=core.checked_path(ROOT/r["mp4_path"],OWNER).parents[3].parent
    require(work.name=="render-"+rid,"Wrong work ID")
    record=core.load_record({rid:binding},rid)
    for key in ("record_sha256","math_sha256"):
        require(r[key]==parent[key]==binding[key],"Changed math/record binding")
    require(r["source_sha256"]==binding["source_sha256"],"Wrong source binding")
    formulas,locations=native.formula_inventory(record)
    inv=work/"formula-inventory.json"
    require(sha(inv)==r["formula_inventory_sha256"],"Inventory changed")
    require(json.loads(inv.read_text("utf-8"))=={"unique_formulas":formulas,"source_occurrences":locations},"Formula omission/rewrite")
    scene=work/"scene.py";require(sha(scene)==r["scene_py_sha256"],"Scene changed")
    tree=ast.parse(scene.read_text("utf-8"))
    literal=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name)and t.id=="FORMULAS" for t in n.targets))
    require(literal==formulas,"Scene formula text changed")
    for c in (x for x in ast.walk(tree) if isinstance(x,ast.Call)):
        if isinstance(c.func,ast.Name) and c.func.id=="MathTex":
            require(isinstance(c.args[0],ast.Name)and c.args[0].id=="formula","Wrong MathTex argument")
            require(any(k.arg=="font_size" and isinstance(k.value,ast.Constant) and k.value.value==48 for k in c.keywords),"Wrong font")
        if isinstance(c.func,ast.Attribute)and c.func.attr in ("scale","resize"):
            require(isinstance(c.func.value,ast.Name)and c.func.value.id=="label","Mathematical glyphs rescaled")
    cache=work/"cache-provenance.json";require(sha(cache)==r["cache_provenance_sha256"],"Cache provenance changed")
    cr=json.loads(cache.read_text("utf-8"));require(cr["parent_manifest_sha256"]==PARENT_SHA,"Wrong cache parent")
    for row in cr["files"]:
        source=core.checked_path(ROOT/row["source"],PARENT)
        require(source.relative_to(PARENT).as_posix() in ARTIFACTS,"Unbound cached source")
        require(sha(source)==ARTIFACTS[source.relative_to(PARENT).as_posix()]["sha256"]==row["sha256"],"Wrong bound cache hash")
        dest=core.checked_path(ROOT/row["destination"],work/"media/Tex")
        require(sha(dest)==row["sha256"],"Copied cache changed")
    gp=work/"page-geometry.json";require(sha(gp)==r["geometry_sha256"],"Geometry changed")
    g=json.loads(gp.read_text("utf-8"))
    require(g["id"]==rid and (g["pixel_width"],g["pixel_height"])==(3840,2160),"Wrong geometry identity/resolution")
    require(F(g["fps"])==1 and F(g["page_seconds"])==3,"Wrong static page timing")
    pages=prior.verify_geometry(g,len(formulas));require(pages==r["page_count"]==len(r["frames"]),"Wrong page count")
    require(len({f["path"] for f in r["frames"]})==pages,"Repeated screenshot")
    metrics=[]
    for page,f in zip(g["pages"],r["frames"]):
        path=core.checked_path(ROOT/f["path"],work/"pages")
        require(path.name==page["frame"] and sha(path)==f["sha256"],"Wrong frame/hash")
        require(f["video_frame_index"]==3*(page["page"]-1) and F(f["video_time_seconds_exact"])==3*(page["page"]-1),"Wrong frame binding")
        metrics.append({"page":page["page"],**page_density(path,len(page["items"]))})
    video=core.checked_path(ROOT/r["mp4_path"],work)
    require(sha(video)==r["mp4_sha256"],"Video changed")
    total=0;matches=0
    with av.open(str(video)) as container:
        stream=container.streams.video[0]
        require((stream.width,stream.height)==(3840,2160) and F(stream.average_rate)==1,"Actual video not native 4K 1fps")
        for frame in container.decode(stream):
            require(F(frame.pts)*F(frame.time_base)==total,"Noncontiguous video timestamp")
            if total%3==0:
                index=total//3;require(index<pages,"Extra video page")
                path=core.checked_path(ROOT/r["frames"][index]["path"],work/"pages")
                with Image.open(path)as im:stored=np.array(im.convert("RGB"))
                actual=np.array(frame.to_image().convert("RGB"))
                require(np.array_equal(actual,stored),"Screenshot differs from actual encoded video pixels")
                matches+=1
            total+=1
    require(total==pages*3==r["video_frames"] and matches==pages,"Missing/extra video frames")
    return {"id":rid,"status":"PASS_BOUND_NATIVE_4K_SOURCE_LAYOUT_AND_PAGE_PIXELS",
            "record_sha256":binding["record_sha256"],"math_sha256":binding["math_sha256"],
            "source_sha256":binding["source_sha256"],"unique_formulas":len(formulas),
            "source_formula_occurrences":len(locations),"page_count":pages,"segment_pages":sum(p["kind"]=="FORMULA_SEGMENT"for p in g["pages"]),
            "mp4_path":r["mp4_path"],"mp4_sha256":r["mp4_sha256"],
            "geometry_path":gp.relative_to(ROOT).as_posix(),"geometry_sha256":sha(gp),
            "formula_inventory_path":inv.relative_to(ROOT).as_posix(),"formula_inventory_sha256":sha(inv),
            "pixel_width":3840,"pixel_height":2160,"fps":"1","page_seconds":"3","video_frames":total,
            "canonical_frames":r["frames"],"page_metrics":metrics,
            "full_glyph_visual_acceptance":"NOT_ESTABLISHED","conceptual_animation":"NOT_EVALUATED","production":"CLOSED"}

PARENT_SHA="5e20929a3b6b72331c4b5b4ba6f9bad4a6d0ca9045cd2dd1bdb00db111d0f016"
ARTIFACTS={}
def main():
    global ARTIFACTS
    require(sha(PARENT/"delivery-manifest.json")==PARENT_SHA,"Parent manifest changed")
    m=json.loads((PARENT/"delivery-manifest.json").read_text("utf-8"))
    ARTIFACTS={a["path"]:a for a in m["artifacts"]}
    for rel,a in ARTIFACTS.items():
        p=core.checked_path(PARENT/rel,PARENT);require(sha(p)==a["sha256"] and p.stat().st_size==a["bytes"],"Parent artifact changed")
    require(sha(PARENT/"DELIVERY_INDEX.jsonl")=="78ef0981a1ac4db8edb5f44ac31202b6e7b99074312e4f710f420ce5dc825d59","Parent index changed")
    parents={r["id"]:r for r in (json.loads(l)for l in (PARENT/"DELIVERY_INDEX.jsonl").read_text("utf-8").splitlines())}
    bindings={r["id"]:r for r in core.load_record_bindings()}
    results=[]
    for i in range(1,4):
        shard=OWNER/("shard-"+str(i));data=json.loads((shard/"receipt.json").read_text("utf-8"))
        require(data["summary"]=={"total":55,"passed":55,"failed":0},"Incomplete/failed shard")
        require(sha(shard/"generator-snapshot.py")==sha(ROOT/"tools/hd_formula_pages.py"),"Generator snapshot changed")
        results.extend(data["results"])
    require(len(results)==165 and len({r["id"]for r in results})==165 and {r["id"]for r in results}==set(parents),"Incomplete/duplicate 165 coverage")
    audits=[]
    for r in results:
        audits.append(verify_one(r,parents[r["id"]],bindings[r["id"]]))
        if len(audits)%15==0:print("Verified native 4K:",len(audits),flush=True)
    (OWNER/"DELIVERY_INDEX.jsonl").write_bytes(b"".join((json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n").encode("utf-8")for r in audits))
    metrics=[m for r in audits for m in r["page_metrics"]]
    summary={"records":165,"pages":sum(r["page_count"]for r in audits),"segment_pages":sum(r["segment_pages"]for r in audits),
             "unique_formula_items_per_record":sum(r["unique_formulas"]for r in audits),
             "source_formula_occurrences":sum(r["source_formula_occurrences"]for r in audits),
             "video_frames":sum(r["video_frames"]for r in audits),"pixel_resolution":[3840,2160],"static_fps":"1",
             "minimum_slot_proxy_at_1080p_exact":str(min(F(m["slot_proxy_at_1080p_exact"]) for m in metrics)),
             "slot_proxy_below_24_count":sum(F(m["slot_proxy_at_1080p_exact"])<24 for m in metrics),
             "slot_proxy_limit":"Not a minimum-glyph-size certificate",
             "status":"PASS_BOUND_NATIVE_4K_SOURCE_LAYOUT_AND_PAGE_PIXELS","all_record_math_and_scene_text":"UNCHANGED",
             "full_glyph_visual_acceptance":"NOT_ESTABLISHED","conceptual_animation":"NOT_EVALUATED",
             "semantic_isolation":"NOT_ESTABLISHED","native_sandbox":"UNVERIFIED","production":"CLOSED","PASS_CORE_SCOPE_issued":False}
    (OWNER/"independent-hd-summary.json").write_bytes(core.encoded(summary));print(json.dumps(summary),flush=True)
if __name__=="__main__":main()
