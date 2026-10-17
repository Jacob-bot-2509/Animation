"""首批 10 题送入受审查 AppContainer 传输做真实渲染试点(逐题超时,可续跑)。

使用 src/animtrain/sandbox_execution.run_code:AppContainer + JobObject,无宿主 fallback。
逐题超时记录,不把超时/失败当成功;本脚本不宣称 43 项联合验收或生产就绪。

用法:
  python run_ten.py [--timeout 120] [--skip-existing] [--ids a,b]
输出:
  runs/render-pilot/results.json、<id>.mp4、<id>-fN.png
"""
import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(r"D:\Animation-Model-Training")
sys.path.insert(0, str(ROOT / "src"))
from animtrain.sandbox_execution import decode_video, run_code  # noqa: E402

PACKS = (ROOT / "reviews/data-prep/2026-10-17-submission/asset-evidence"
         "/presentation-pipeline/runs/review-packs")
OUT = PACKS.parent / "render-pilot"
OUT.mkdir(parents=True, exist_ok=True)
RESULTS = OUT / "results.json"
FRACTIONS = (0.25, 0.5, 0.75)


def load_results() -> dict:
    if RESULTS.is_file():
        try:
            return json.loads(RESULTS.read_text(encoding="utf-8"))
        except ValueError:
            pass
    return {"schema": "render-pilot-v1", "packs": [],
            "note": "AppContainer pilot; not 43-point acceptance, not R/E evidence"}


def save_results(doc: dict) -> None:
    tmp = RESULTS.with_suffix(".tmp")
    tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(RESULTS)


def extract_frames(mp4: Path, sid: str) -> list[str]:
    try:
        import av
    except Exception as exc:
        return [f"frame_extract_unavailable: {exc}"]
    try:
        with av.open(str(mp4)) as c:
            total = sum(1 for _ in c.decode(video=0))
        if total <= 0:
            return ["no_decoded_frames"]
        wants = {max(0, min(total - 1, int(total * f))) for f in FRACTIONS}
        saved = []
        with av.open(str(mp4)) as c:
            for idx, frame in enumerate(c.decode(video=0)):
                if idx in wants:
                    name = f"{sid}-f{idx}.png"
                    frame.to_image().save(OUT / name)
                    saved.append(name)
        return saved
    except Exception as exc:
        return [f"frame_extract_error: {type(exc).__name__}: {exc}"]


def render_one(sid: str, timeout_ms: int) -> dict:
    pack = PACKS / sid
    src = (pack / "scene_runnable.py").read_text(encoding="utf-8")
    if "class Candidate(Scene):" not in src:
        return {"sample_id": sid, "status": "skipped_no_candidate_class"}
    code = src.replace("class Candidate(Scene):", "class ConceptScene(Scene):")
    started = time.time()
    row = {"sample_id": sid, "elapsed_s": None}
    try:
        res = run_code(code, timeout_ms=timeout_ms)
    except subprocess.TimeoutExpired as exc:
        row.update(status="timeout", ok=False,
                   detail=f"TimeoutExpired after {timeout_ms} ms",
                   work=str(getattr(exc, "work", "")),
                   stderr_tail=(exc.stderr or b"").decode("utf-8", "replace")[-1500:])
    except Exception as exc:
        row.update(status="script_error", ok=False,
                   detail=f"{type(exc).__name__}: {exc}")
    else:
        work = Path(res["work"])
        row.update(work=str(work), rc=res["rc"],
                   source_sha256=res["source_sha256"],
                   isolation={"backend": "windows_appcontainer",
                              "job_assigned": res["parent_evidence"].get("job_assigned_before_resume"),
                              "tree_stopped": res["parent_evidence"].get("tree_stopped"),
                              "appcontainer": res["parent_evidence"].get("token", {}).get("is_appcontainer"),
                              "memory_limit_mb": res["parent_evidence"].get("memory_limit_mb"),
                              "network_isolated": False})
        if res["rc"] != 0:
            row.update(status="manim_failed", ok=False,
                       stderr_tail=res["stderr"][-2500:], stdout_tail=res["stdout"][-500:])
        else:
            outputs = [p for p in work.rglob("ConceptScene.mp4")
                       if "partial_movie_files" not in p.parts]
            if len(outputs) != 1:
                row.update(status="no_unique_video", ok=False,
                           detail=f"found {len(outputs)} ConceptScene.mp4")
            else:
                art = decode_video(outputs[0])
                dst = OUT / f"{sid}.mp4"
                shutil.copyfile(art["path"], dst)
                row.update(status="rendered", ok=True, mp4=dst.name,
                           mp4_sha256=art["sha256"], bytes=art["size"],
                           frames=art["frames"], width=art["width"], height=art["height"],
                           frame_rate=art["frame_rate"])
                row["pngs"] = extract_frames(dst, sid)
    row["elapsed_s"] = round(time.time() - started, 1)
    return row


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout", type=int, default=120, help="单题超时秒")
    ap.add_argument("--skip-existing", action="store_true")
    ap.add_argument("--ids", default="")
    args = ap.parse_args()
    ids = ([x.strip() for x in args.ids.split(",") if x.strip()] if args.ids
           else sorted(p.name for p in PACKS.iterdir() if p.is_dir()))
    doc = load_results()
    by_id = {r["sample_id"]: r for r in doc["packs"]}
    for sid in ids:
        if args.skip_existing and by_id.get(sid, {}).get("ok"):
            print(f"SKIP {sid} (already rendered)", flush=True)
            continue
        row = render_one(sid, args.timeout * 1000)
        by_id[sid] = row
        doc["packs"] = [by_id[k] for k in sorted(by_id)]
        save_results(doc)
        print(json.dumps({"id": sid, "status": row["status"], "ok": row.get("ok"),
                          "elapsed_s": row["elapsed_s"],
                          "frames": row.get("frames"), "mp4": row.get("mp4")},
                         ensure_ascii=False), flush=True)
    ok = sum(1 for r in doc["packs"] if r.get("ok"))
    print(f"SUMMARY ok={ok}/{len(doc['packs'])}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
