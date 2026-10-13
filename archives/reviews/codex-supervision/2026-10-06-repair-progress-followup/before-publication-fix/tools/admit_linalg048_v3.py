"""Admit linalg-048 v3 shear candidate: exact math + record-specific render.

Follows the calc-derivative-001 acceptance pattern (three-gates). The
candidate scene is authored for THIS record only — no generic template.
Evidence output: reviews/2026-10-06-linalg048-admission/render-evidence.json
plus final frame PNG. Does NOT modify active data/manifest/locks; that is the
separate apply step.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from animtrain.sandbox_execution import render_scene  # noqa: E402

CANDIDATE_PATH = (ROOT / "reviews/codex-supervision/2026-10-06-holdout-strict-fix"
                  / "linalg048-v3/candidate.json")
CANDIDATE_SHA = "8d30d09d5f1dd5b7c72f429ee5670680f2a84a953fbebd57d8372bfbca56e169"
ACTIVE = ROOT / "data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl"
MANIFEST = ROOT / "data/manifest.json"
OUT_DIR = ROOT / "reviews/2026-10-06-linalg048-admission"

# Record-specific Manim scene for the horizontal shear T(x,y)=(x+3y,y).
# Faithfully implements the candidate's five scene_spec steps.
SCENE_SOURCE = r"""
from manim import *

class ConceptScene(Scene):
    def construct(self):
        title = Text('求矩阵对应的线性变换对二维平面的几何影响',
                     font='Microsoft YaHei', font_size=24, color=WHITE).to_edge(UP)
        formula = MathTex(r'T(x,y)=(x+3y,\,y),\qquad \det A=1',
                          color=WHITE).scale(3/4).next_to(title, DOWN)
        panel = Rectangle(width=8.8, height=3.9, fill_color=GRAY_A,
                          fill_opacity=1, stroke_width=0).shift(DOWN*0.4)
        axes = Axes(x_range=[-0.5, 5.5, 1], y_range=[-0.5, 2.2, 1],
                    x_length=7.4, y_length=2.6,
                    axis_config={'color': BLACK, 'include_numbers': True,
                                 'font_size': 15,
                                 'decimal_number_config': {'color': BLACK,
                                                           'num_decimal_places': 0}})
        axes.move_to(panel.get_center() + DOWN*0.05)

        sq_pts = [(0,0), (1,0), (1,1), (0,1)]
        pa_pts = [(0,0), (1,0), (4,1), (3,1)]
        square = Polygon(*[axes.c2p(*p) for p in sq_pts],
                         color=BLUE, fill_opacity=0.2)
        sq_verts = VGroup(*[Dot(axes.c2p(*p), color=BLUE, radius=0.06)
                            for p in sq_pts])
        para = Polygon(*[axes.c2p(*p) for p in pa_pts],
                       color=ORANGE, fill_opacity=0.2)
        pa_verts = VGroup(*[Dot(axes.c2p(*p), color=ORANGE, radius=0.06)
                            for p in pa_pts])
        pa_labels = VGroup(*[
            MathTex(r'(%d,%d)' % p, color=WHITE).scale(1/2).next_to(
                axes.c2p(*p), UL if p[1] == 0 else UR)
            for p in pa_pts])

        def seg(y):
            dots = VGroup(Dot(axes.c2p(0, y), color=TEAL, radius=0.06),
                          Dot(axes.c2p(1, y), color=TEAL, radius=0.06))
            return VGroup(Line(axes.c2p(0, y), axes.c2p(1, y), color=TEAL), dots)
        seg1, seg1_img = seg(1/2), seg(1/2)
        seg1_img.shift(axes.c2p(3/2, 0) - axes.c2p(0, 0))
        seg2, seg2_img = seg(1), seg(1)
        seg2_img.shift(axes.c2p(3, 0) - axes.c2p(0, 0))
        caption3 = Text('水平直线作为集合不变，线上点位移 (3y, 0)',
                        font='Microsoft YaHei', font_size=20,
                        color=WHITE).to_edge(DOWN)
        caption4 = Text('单位正方形变为底 1 高 1 的平行四边形，面积不变',
                        font='Microsoft YaHei', font_size=20,
                        color=WHITE).to_edge(DOWN)
        vline = Line(axes.c2p(1/2, -0.3), axes.c2p(1/2, 1.2), color=GREEN)
        vline_img = Line(axes.c2p(1/2 - 0.9, -0.3), axes.c2p(1/2 + 3.6, 1.2),
                         color=GREEN)
        vlabel = MathTex(r'X-3Y=c', color=WHITE).scale(1/2).next_to(
            axes.c2p(4.1, 1.2), UR)
        e2_dot = Dot(axes.c2p(0, 1), color=YELLOW, radius=0.07)
        e2_img = Dot(axes.c2p(3, 1), color=YELLOW, radius=0.07)
        e2_label = MathTex(r'\sqrt{10}', color=WHITE).scale(1/2).next_to(
            axes.c2p(3, 1), UR)

        self.add(title, panel)
        self.play(Create(axes))
        self.play(Create(square), Create(sq_verts))
        self.play(Write(formula))
        self.play(Transform(seg1, seg1_img), Transform(seg2, seg2_img),
                  run_time=1.5)
        self.play(Write(caption3))
        self.wait(1/2)
        self.play(Transform(square, para), Transform(sq_verts, pa_verts),
                  run_time=1.5)
        self.play(Write(caption4), Write(pa_labels))
        self.wait(1/2)
        self.play(Create(vline), Create(e2_dot))
        self.play(Transform(vline, vline_img), Write(vlabel),
                  Transform(e2_dot, e2_img), Write(e2_label), run_time=1.5)
        self.wait(1)
"""


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_candidate():
    raw = CANDIDATE_PATH.read_bytes()
    if hashlib.sha256(raw).hexdigest() != CANDIDATE_SHA:
        raise ValueError("candidate hash mismatch")
    return json.loads(raw.decode("utf-8-sig"))


def math_checks(c: dict) -> dict:
    m = re.search(r"\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}", c["problem"])
    if not m:
        raise ValueError("matrix missing")
    A = [[Fraction(x) for x in row.split("&")] for row in m.group(1).split(r"\\")]
    assert A == [[1, 3], [0, 1]], "matrix mismatch"
    def T(p):
        x, y = p
        return (A[0][0] * x + A[0][1] * y, A[1][0] * x + A[1][1] * y)
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    assert det == 1, "det mismatch"
    imgs = [T(p) for p in [(0, 0), (1, 0), (1, 1), (0, 1)]]
    assert imgs == [(0, 0), (1, 0), (4, 1), (3, 1)], "vertex images mismatch"
    # shoelace oriented area
    area = Fraction(0)
    pts = [(0, 0), (1, 0), (4, 1), (3, 1)]
    for i, (x1, y1) in enumerate(pts):
        x2, y2 = pts[(i + 1) % 4]
        area += x1 * y2 - x2 * y1
    assert area / 2 == 1, "shoelace area mismatch"
    # segment images for c=1/2 and c=1
    for c in (Fraction(1, 2), Fraction(1)):
        assert T((0, c)) == (3 * c, c) and T((1, c)) == (1 + 3 * c, c)
    # vertical line x=c -> X-3Y=c, slope 1/3
    assert T((Fraction(1, 2), 0)) == (Fraction(1, 2), 0)
    assert T((Fraction(1, 2), 1)) == (Fraction(7, 2), 1), "vline image mismatch"
    # e2 image norm
    assert T((0, 1)) == (3, 1)
    return {"matrix": [["1", "3"], ["0", "1"]], "det": "1",
            "vertex_images": [list(map(str, p)) for p in imgs],
            "shoelace_area": "1",
            "segment_images_c12": ["3/2", "5/2"],
            "segment_images_c1": ["3", "4"],
            "vline_image": "X-3Y=c",
            "e2_image": "(3,1)",
            "e2_norm_squared": "10"}


def main() -> int:
    try:
        cand = load_candidate()
        checks = math_checks(cand)
        active = json.loads(ACTIVE.read_text("utf-8-sig").splitlines()[0])
        assert active.get("id") == "linalg-048", "line 1 is not linalg-048"
        manifest = json.loads(MANIFEST.read_text("utf-8"))
        entry = next(e for e in manifest["entries"] if e["path"].endswith("dataset_linalg.jsonl"))
        assert sha(ACTIVE) == entry["sha256"], "active file hash mismatch"
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        evidence_path = OUT_DIR / "render-evidence.json"
        if evidence_path.exists():
            raise ValueError("evidence output exists")
        print("math checks ok; rendering scene in AppContainer ...", flush=True)
        result = render_scene(SCENE_SOURCE)
        if not result.get("ok"):
            print("[FAIL] render:", result.get("detail"))
            return 1
        out = result["output"]["path"]
        import av
        with av.open(out) as c:
            frames = list(c.decode(video=0))
        final_png = OUT_DIR / "linalg048-final-frame-v3.png"
        frames[-1].to_image().save(final_png)
        evidence = {
            "schema": "linalg048-admission-render-v1",
            "candidate_sha256": sha(CANDIDATE_PATH),
            "candidate_raw_sha256": CANDIDATE_SHA,
            "active_record_sha256": hashlib.sha256(
                ACTIVE.read_text("utf-8-sig").splitlines()[0].encode("utf-8")).hexdigest(),
            "manifest_sha256": sha(MANIFEST),
            "math_checks": checks,
            "semantic_review": (
                "Read full problem/solution/answer and all 5 scene steps. "
                "T(x,y)=(x+3y,y): x-axis fixed; horizontal line SETS invariant with "
                "point displacement (3y,0); segments [0,1]x{c} -> [3c,1+3c]x{c}; "
                "vertical x=c -> X-3Y=c slope 1/3; unit square -> parallelogram "
                "(0,0),(1,0),(4,1),(3,1) with shoelace area 1 = det A; "
                "||T(0,1)|| = sqrt(10) shows length not preserved. No generic "
                "geometry; five steps match the derivation one-to-one."),
            "render": {"ok": result["ok"], "detail": result["detail"],
                       "frames": len(frames),
                       "media_path": str(out),
                       "final_frame_png": str(final_png),
                       "isolation": result.get("isolation")},
        }
        evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8", newline="\n")
        print(json.dumps({"render_ok": True, "frames": len(frames),
                          "final_frame": str(final_png),
                          "evidence": str(evidence_path)}, ensure_ascii=False))
        return 0
    except Exception as exc:
        print("[FAIL]", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
