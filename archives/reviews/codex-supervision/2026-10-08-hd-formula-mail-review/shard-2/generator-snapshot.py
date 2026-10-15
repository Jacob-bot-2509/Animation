"""True 4K exact-formula pages from a pinned, fully bound vector-cache parent."""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys, time
from fractions import Fraction
from pathlib import Path
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0,str(Path(__file__).resolve().parent))
import core_signatures as core
import native_render_pilot as native
import readable_formula_pages as base
PARENT=core.ROOT/"reviews/codex-supervision/2026-10-08-visual-mail-review"
PARENT_SHA="5e20929a3b6b72331c4b5b4ba6f9bad4a6d0ca9045cd2dd1bdb00db111d0f016"
INDEX_SHA="78ef0981a1ac4db8edb5f44ac31202b6e7b99074312e4f710f420ce5dc825d59"
BASE_SHA="64eda4c2b4047c40cdf6339d59a26f6b5fca384ecfd8879be15f009ce7b3e0a7"
WIDTH,HEIGHT,FPS,PAGE_SECONDS=3840,2160,1,3

def pinned(path,expected):
    data=path.read_bytes()
    if core.digest(data)!=expected:raise ValueError("Pinned input changed: "+str(path))
    return data

def load_parent():
    manifest=json.loads(pinned(PARENT/"delivery-manifest.json",PARENT_SHA))
    artifacts={}
    for row in manifest["artifacts"]:
        p=core.checked_path(PARENT/row["path"],PARENT)
        if row["path"] in artifacts or p==PARENT/"delivery-manifest.json":raise ValueError("Invalid parent manifest")
        pinned(p,row["sha256"])
        if p.stat().st_size!=row["bytes"]:raise ValueError("Parent byte count changed")
        artifacts[row["path"]]=row
    raw=pinned(PARENT/"DELIVERY_INDEX.jsonl",INDEX_SHA)
    rows=[json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]
    if len(rows)!=165 or len({r["id"] for r in rows})!=165:raise ValueError("Parent coverage changed")
    pinned(Path(base.__file__),BASE_SHA)
    return {r["id"]:r for r in rows},artifacts

def copy_bound_cache(parent_row,artifacts,destination):
    geometry=core.checked_path(core.ROOT/parent_row["geometry_path"],PARENT)
    pinned(geometry,parent_row["geometry_sha256"])
    folder=geometry.parent/"media/Tex"
    destination.mkdir(parents=True,exist_ok=False)
    receipts=[]
    for source in sorted(folder.iterdir()):
        if source.suffix not in (".svg",".tex"):continue
        source=core.checked_path(source,PARENT)
        rel=source.relative_to(PARENT).as_posix()
        if rel not in artifacts:raise ValueError("Unbound vector cache")
        data=pinned(source,artifacts[rel]["sha256"])
        target=destination/source.name
        target.write_bytes(data)
        receipts.append({"source":source.relative_to(core.ROOT).as_posix(),
                         "destination":target.relative_to(core.ROOT).as_posix(),
                         "sha256":core.digest(data),"bytes":len(data)})
    if not any(Path(r["source"]).suffix==".svg" for r in receipts):raise ValueError("No bound vector cache")
    return receipts

def hd_scene(formulas,rid):
    source=base.scene_source(formulas,rid)
    return source.replace('"schema":"exact-formula-pages-v1"',
                          '"schema":"exact-formula-pages-hd-v1","pixel_width":config.pixel_width,"pixel_height":config.pixel_height,"fps":str(config.frame_rate),"page_seconds":"3"')

def render_command(scene,media):
    return [str(native.PY),"-B","-m","manim","render",str(scene),"ConceptScene","-ql",
            "--resolution",str(WIDTH)+","+str(HEIGHT),"--fps",str(FPS),
            "--media_dir",str(media),"--disable_caching"]

def decode_pages(video,folder,expected):
    import av
    if type(expected)is not int or expected<=0:raise ValueError("Invalid page count")
    folder.mkdir(exist_ok=False)
    total=0;frames=[]
    with av.open(str(video)) as container:
        stream=container.streams.video[0]
        if (stream.width,stream.height)!=(WIDTH,HEIGHT) or Fraction(stream.average_rate)!=FPS:
            raise ValueError("Actual video is not native 4K at selected fps")
        for frame in container.decode(stream):
            if total%(FPS*PAGE_SECONDS)==0:
                page=total//(FPS*PAGE_SECONDS)
                if page>=expected or Fraction(frame.pts)*Fraction(frame.time_base)!=page*PAGE_SECONDS:
                    raise ValueError("Wrong encoded page timing")
                image=frame.to_image()
                if image.size!=(WIDTH,HEIGHT):raise ValueError("Wrong decoded dimensions")
                path=folder/("page-"+str(page+1).zfill(3)+".png")
                image.save(path)
                frames.append({"path":path.relative_to(core.ROOT).as_posix(),"sha256":core.digest(path.read_bytes()),
                               "video_frame_index":total,"video_time_seconds_exact":str(page*PAGE_SECONDS)})
            total+=1
    if total!=expected*FPS*PAGE_SECONDS:raise ValueError("Missing/extra actual video frames")
    return frames,total

def render(rid,work,record,binding,parent,artifacts):
    work.mkdir(exist_ok=False)
    formulas,locations=native.formula_inventory(record)
    inventory={"unique_formulas":formulas,"source_occurrences":locations}
    old=pinned(core.checked_path(core.ROOT/parent["formula_inventory_path"],PARENT),parent["formula_inventory_sha256"])
    if json.loads(old)!=inventory:raise ValueError("Formula/source inventory changed")
    scene=work/"scene.py";scene.write_text(hd_scene(formulas,rid),encoding="utf-8",newline="\n")
    (work/"formula-inventory.json").write_bytes(core.encoded(inventory))
    cache=copy_bound_cache(parent,artifacts,work/"media/Tex")
    (work/"cache-provenance.json").write_bytes(core.encoded({"parent_manifest_sha256":PARENT_SHA,"files":cache}))
    command=render_command(scene,work/"media")
    start=time.monotonic_ns()
    try:
        p=subprocess.run(command,capture_output=True,cwd=work,timeout=600)
        rc,out,err,timeout=p.returncode,p.stdout,p.stderr,False
    except subprocess.TimeoutExpired as exc:
        rc,out,err,timeout=-1,native.as_bytes(exc.stdout),native.as_bytes(exc.stderr),True
    (work/"stdout.bin").write_bytes(out);(work/"stderr.bin").write_bytes(err)
    videos=list((work/"media").rglob("ConceptScene.mp4"));frames=[];count=0;g={}
    if rc==0 and len(videos)==1 and not timeout:
        try:
            g=json.loads((work/"page-geometry.json").read_text("utf-8"))
            if (g["pixel_width"],g["pixel_height"])!=(WIDTH,HEIGHT) or Fraction(g["fps"])!=FPS:
                raise ValueError("Wrong renderer configuration")
            frames,count=decode_pages(videos[0],work/"pages",len(g["pages"]))
        except (ValueError,OSError,KeyError,IndexError) as exc:
            (work/"export-error.json").write_bytes(core.encoded({"error":str(exc)}))
    ok=rc==0 and not timeout and bool(frames) and len(frames)==len(g.get("pages",[]))
    receipt={"id":rid,"status":"PASS_BOUND_HD_RENDER" if ok else "FAIL_BOUND_HD_RENDER",
             "rc":rc,"timed_out":timeout,"command":command,
             "elapsed_seconds_exact":str(Fraction(time.monotonic_ns()-start,10**9)),
             **{k:binding[k] for k in ("source_sha256","record_sha256","math_sha256")},
             "core_manifest_sha256":core.CORE_MANIFEST_SHA256,"parent_manifest_sha256":PARENT_SHA,
             "scene_py_sha256":core.digest(scene.read_bytes()),
             "formula_inventory_sha256":core.digest((work/"formula-inventory.json").read_bytes()),
             "cache_provenance_sha256":core.digest((work/"cache-provenance.json").read_bytes()),
             "unique_formulas":len(formulas),"source_formula_occurrences":len(locations),
             "pixel_width":WIDTH,"pixel_height":HEIGHT,"fps":str(FPS),"page_seconds":str(PAGE_SECONDS),
             "page_count":len(frames),"video_frames":count,"font_size":48,"formula_scale":"1",
             "frames":frames,"page_capture":"DECODED_ACTUAL_4K_VIDEO_NO_UPSCALE",
             "mp4_path":videos[0].relative_to(core.ROOT).as_posix() if len(videos)==1 else None,
             "mp4_sha256":core.digest(videos[0].read_bytes()) if len(videos)==1 else None,
             "geometry_sha256":core.digest((work/"page-geometry.json").read_bytes()) if g else None,
             "full_glyph_visual_acceptance":"NOT_ESTABLISHED","conceptual_animation":"NOT_EVALUATED",
             "native_sandbox":"UNVERIFIED","semantic_isolation":"NOT_ESTABLISHED","production":"CLOSED"}
    (work/"receipt.json").write_bytes(core.encoded(receipt))
    return receipt

def run(ids,out):
    parents,artifacts=load_parent()
    ids=ids or list(parents)
    if not ids or len(ids)!=len(set(ids)):raise ValueError("Unique nonempty IDs required")
    bindings={r["id"]:r for r in core.load_record_bindings()}
    for rid in ids:
        if rid not in parents or rid not in bindings:raise ValueError("Unknown bound record")
        for key in ("record_sha256","math_sha256"):
            if parents[rid][key]!=bindings[rid][key]:raise ValueError("Current math binding changed")
        core.load_record(bindings,rid)
    core.publish(out,{"run-inputs.json":core.encoded({"ids":ids,"parent_manifest_sha256":PARENT_SHA,
        "parent_index_sha256":INDEX_SHA,"base_generator_sha256":BASE_SHA,"generator_sha256":core.digest(Path(__file__).read_bytes()),
        "core_manifest_sha256":core.CORE_MANIFEST_SHA256,"bindings":[bindings[rid] for rid in ids]}),
        "generator-snapshot.py":Path(__file__).read_bytes()})
    results=[]
    for rid in ids:
        r=render(rid,out/("render-"+rid),core.load_record(bindings,rid),bindings[rid],parents[rid],artifacts)
        results.append(r)
        print(json.dumps({k:r[k] for k in ("id","status","rc","page_count")}),flush=True)
    summary={"total":len(results),"passed":sum(r["status"]=="PASS_BOUND_HD_RENDER" for r in results)}
    summary["failed"]=summary["total"]-summary["passed"]
    (out/"receipt.json").write_bytes(core.encoded({"results":results,"summary":summary,"production":"CLOSED"}))
    return 0 if not summary["failed"] else 3

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("--ids",nargs="+")
    ap.add_argument("--out",type=Path,required=True);a=ap.parse_args()
    try:return run(a.ids,a.out.absolute())
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print(json.dumps({"status":"FAIL_HD_BOUND_INPUT","error":str(exc),"production":"CLOSED"}));return 2
if __name__=="__main__":raise SystemExit(main())
