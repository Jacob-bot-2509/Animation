"""汇总十题渲染试点结果(表格 + 总 SHA 清单)。"""
import hashlib
import json
from pathlib import Path

PILOT = Path(r"D:\Animation-Model-Training\reviews\data-prep\2026-10-17-submission"
             r"\asset-evidence\presentation-pipeline\runs\render-pilot")
doc = json.loads((PILOT / "results.json").read_text(encoding="utf-8"))
ok = [r for r in doc["packs"] if r.get("ok")]
print(f"rendered {len(ok)}/{len(doc['packs'])}")
print(f"{'sample':<26} {'status':<9} {'s':>6} {'frames':>6} {'size':>8}  sha12  mp4")
for r in doc["packs"]:
    print(f"{r['sample_id']:<26} {str(r.get('status')):<9} {str(r.get('elapsed_s')):>6} "
          f"{str(r.get('frames')):>6} {str(r.get('bytes')):>8}  "
          f"{str(r.get('mp4_sha256'))[:12]}  {r.get('mp4')}")
print("all 45 frames:", all(r.get("frames") == 45 for r in ok))
print("all 854x480:", all((r.get("width"), r.get("height")) == (854, 480) for r in ok))
total = sum(r.get("bytes", 0) for r in ok)
print("total bytes:", total)
manifest = {r["sample_id"]: {"mp4_sha256": r.get("mp4_sha256"), "bytes": r.get("bytes"),
                             "frames": r.get("frames")} for r in doc["packs"]}
(PILOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                     encoding="utf-8")
print("manifest:", hashlib.sha256((PILOT / "manifest.json").read_bytes()).hexdigest())
