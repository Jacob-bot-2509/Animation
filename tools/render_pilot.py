"""渲染试点:scene_spec v2 → 模板路由 → Manim 场景 → 媒体产物(正常环境)。

目的:验证"数据集记录→场景代码→可渲染媒体"整条管线可行,并记录产物
哈希/尺寸供复现。产物输出 .render-pilot/<run_id>/。仅正常环境(非沙箱);
沙箱渲染按分工由复查方接线后另行验收。

用法:
  .venv/Scripts/python.exe -X utf8 tools/render_pilot.py \
      --limit 8 --format png [--records data/v2/eval/dataset_eval.json ...]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import render_templates as rt  # noqa: E402

OUT = ROOT / ".render-pilot"
MANIM_TIMEOUT_S = 120


def _load_records(paths: list[Path]) -> list[dict]:
    recs = []
    for p in paths:
        data = json.loads(p.read_text(encoding="utf-8"))
        recs.extend(data if isinstance(data, list) else [])
    return recs


def _stratify(recs: list[dict], limit: int) -> list[dict]:
    """按 category 分组轮转抽样,保证试点覆盖各模块。"""
    by_cat: dict[str, list[dict]] = {}
    for rec in recs:
        by_cat.setdefault(rec.get("category", "未知"), []).append(rec)
    picks: list[dict] = []
    while len(picks) < limit and by_cat:
        for cat in list(by_cat.keys()):
            if by_cat[cat]:
                picks.append(by_cat[cat].pop(0))
                if len(picks) >= limit:
                    break
            else:
                del by_cat[cat]
    return picks


def _media_info(base: Path) -> list[dict]:
    out = []
    for f in sorted(base.rglob("*")) if base.exists() else []:
        if f.is_file():
            out.append({"path": str(f.relative_to(base)),
                        "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
                        "size": f.stat().st_size})
    return out


def _render_one(rec: dict, scene_dir: Path, media_base: Path, fmt: str,
                py: str) -> dict:
    scene_src = rt.build_scene(rec)
    scene_path = scene_dir / "scene.py"
    scene_path.write_text(scene_src, encoding="utf-8")
    cmd = [py, "-X", "utf8", "-m", "manim", "render", "-ql",
           f"--format={fmt}", "--media_dir", str(media_base),
           str(scene_path), "PilotScene"]
    try:
        cp = subprocess.run(cmd, capture_output=True, cwd=scene_dir,
                            timeout=MANIM_TIMEOUT_S)
        rc = cp.returncode
        out_tail = (cp.stdout + cp.stderr).decode("utf-8", "replace")[-1500:]
    except subprocess.TimeoutExpired as e:
        rc = None
        out_tail = "TIMEOUT: " + repr(e)
    return {"template": rt.route(rec),
            "scene_sha256": hashlib.sha256(scene_src.encode("utf-8")).hexdigest(),
            "rc": rc, "out_tail": out_tail,
            "media": _media_info(media_base),
            "command": cmd}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--format", choices=["png", "mp4"], default="png")
    parser.add_argument("--records", nargs="*", type=Path,
                        default=[ROOT / "data/v2/eval/dataset_eval.json",
                                 ROOT / "data/v2/test/dataset_test.json"])
    args = parser.parse_args(argv)
    recs = _load_records(args.records)
    picks = _stratify(recs, args.limit)
    run_id = uuid.uuid4().hex[:10]
    base = OUT / run_id
    py = str(ROOT / ".venv" / "Scripts" / "python.exe")
    results = {"run_id": run_id, "format": args.format,
               "manim": "0.21.0(venv)", "command": [sys.executable] + sys.argv,
               "count": len(picks), "records": []}
    for i, rec in enumerate(picks):
        scene_dir = base / f"scene-{i:02d}"
        media_base = base / f"media-{i:02d}"
        scene_dir.mkdir(parents=True, exist_ok=True)
        item = {"id": rec.get("solution_id") or rec.get("id"),
                "problem_id": rec.get("problem_id"),
                "category": rec.get("category"),
                "problem": rec.get("problem", "")[:120]}
        item.update(_render_one(rec, scene_dir, media_base, args.format, py))
        results["records"].append(item)
        print(json.dumps({"id": item["id"], "template": item["template"],
                          "rc": item["rc"],
                          "media_count": len(item["media"])},
                         ensure_ascii=False), flush=True)
    results["summary"] = {
        "ok": sum(1 for r in results["records"] if r["rc"] == 0),
        "fail": sum(1 for r in results["records"] if r["rc"] != 0),
        "templates": {t: sum(1 for r in results["records"]
                             if r["template"] == t)
                      for t in sorted({r["template"] for r in results["records"]})}}
    out = base / "pilot-report.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(json.dumps(results["summary"], ensure_ascii=False))
    print("report:", out)
    return 0 if results["summary"]["fail"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
