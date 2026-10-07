"""原生渲染试点:当前核心修订记录 → 模板生成 Manim 场景 → venv 原生渲染(可信固定样例先行).

口径:本地可信样例渲染,验证 LaTeX/MiKTeX/Pango 真实渲染;不是生产传输证据
(生产门 CLOSED,AppContainer 证书未签发),回执如实 LOCAL_RENDER_ONLY。
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "reviews/codex-supervision/2026-10-07-semantic-signature-supervision/effective-core-v2"
OUT = ROOT / "reviews/2026-10-07-native-render-pilot"
PY = ROOT / ".venv/Scripts/python.exe"
MATH_SPLIT = re.compile(r"\$([^$]+)\$")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_record(rid: str) -> tuple[dict, dict]:
    rows = [json.loads(l) for l in (CORE / "record-bindings.jsonl").read_text(encoding="utf-8-sig").splitlines()
            if l.strip()]
    b = next((r for r in rows if r["id"] == rid), None)
    if b is None:
        raise ValueError("unknown id: " + rid)
    lines = (ROOT / b["path"]).read_bytes().splitlines(keepends=True)
    rec = json.loads(lines[b["source_line"] - 1].decode("utf-8-sig"))
    return rec, b


def build_scene(rec: dict) -> str:
    """模板场景:先建全部 MathTex(修复顺序),再 Text 标签;不做动画."""
    formulas = []
    for field in ("problem", "solution", "answer"):
        text = rec.get(field) or ""
        formulas.extend(m for m in MATH_SPLIT.findall(text) if len(m) <= 200)
    spec = rec.get("scene_spec")
    if isinstance(spec, dict):
        for s in list(spec.get("objects") or []) + list(spec.get("steps") or []):
            formulas.extend(m for m in MATH_SPLIT.findall(s) if len(m) <= 200)
    # 去重保序
    seen, unique = set(), []
    for f in formulas:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    lines = [
        "from manim import *",
        "import numpy as np",
        "class ConceptScene(Scene):",
        "    def construct(self):",
        "        # 修复顺序:所有 MathTex 先编译,再渲染 Text(Pango)",
        "        maths = [MathTex(r'%s') for r in ["
        % "",
    ]
    body = []
    for f in unique:
        body.append("            " + repr(f) + ",")
    if not body:
        body.append("            '\\\\text{(无公式)}',")
    lines.append("\n".join(body))
    lines.append("        ]]")
    lines.append("        group = VGroup(*maths)")
    lines.append("        group.arrange(DOWN, buff=0.25).scale_to_fit_width(config.frame_width - 1)")
    lines.append("        self.add(group)")
    lines.append("        label = Text('trusted-sample-render', font_size=24).to_corner(UL)")
    lines.append("        self.add(label)")
    lines.append("        self.wait(0.2)")
    return "\n".join(lines) + "\n"


def render_one(rid: str, work: Path) -> dict:
    rec, binding = load_record(rid)
    code = build_scene(rec)
    scene_file = work / "scene.py"
    scene_file.write_text(code, encoding="utf-8", newline="\n")
    t0 = time.monotonic()
    try:
        proc = subprocess.run(
            [str(PY), "-m", "manim", "render", str(scene_file), "ConceptScene",
             "-ql", "--media_dir", str(work / "media"), "--disable_caching"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=240, cwd=str(work))
        rc, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        rc, stdout, stderr, timed_out = -1, "", (exc.stdout or "") + (exc.stderr or ""), True
    mp4s = list((work / "media").rglob("ConceptScene.mp4"))
    result = {
        "id": rid, "rc": rc, "timed_out": timed_out,
        "elapsed_s": round(time.monotonic() - t0, 1),
        "mp4": len(mp4s) == 1,
        "mp4_path": str(mp4s[0].relative_to(work)) if len(mp4s) == 1 else None,
        "record_sha256": binding["record_sha256"],
        "math_sha256": binding["math_sha256"],
        "scene_py_sha256": digest(scene_file.read_bytes()),
        "stderr_tail": stderr[-400:],
    }
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ids", nargs="+", required=True)
    ap.add_argument("--batch")
    args = ap.parse_args(argv)
    batch = args.batch or "pilot"
    if not re.fullmatch(r"[a-z0-9-]{1,60}", batch):
        raise ValueError("invalid batch name")
    bdir = OUT / batch
    bdir.mkdir(parents=True, exist_ok=True)
    results = []
    for rid in args.ids:
        work = bdir / f"render-{rid}"
        work.mkdir(parents=True, exist_ok=True)
        r = render_one(rid, work)
        results.append(r)
        print(f"[{rid}] rc={r['rc']} mp4={r['mp4']} {r['elapsed_s']}s")
    receipt = {
        "schema": "native-render-pilot-v1",
        "batch": batch, "renderer": "claude-code",
        "transport": "LOCAL_VENV_MANIM_TRUSTED_SAMPLE",
        "production_evidence": False,
        "note": "可信固定样例本地原生渲染;生产门CLOSED,此回执不构成生产传输/隔离证据;"
                "场景为模板生成(先MathTex后Text,修复顺序),验证修订版LaTeX真实渲染",
        "results": results,
        "summary": {
            "total": len(results),
            "rendered": sum(1 for r in results if r["mp4"] and r["rc"] == 0),
            "failed": sum(1 for r in results if not r["mp4"] or r["rc"] != 0),
        },
    }
    with (bdir / "receipt.json").open("w", encoding="utf-8", newline="\n") as f:
        json.dump(receipt, f, ensure_ascii=False, indent=2)
        f.write("\n")
    b = (bdir / "receipt.json").read_bytes()
    print(f"回执: {(bdir / 'receipt.json').relative_to(ROOT)}  sha256={digest(b)}  bytes={len(b)}")
    print(f"汇总: {receipt['summary']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
