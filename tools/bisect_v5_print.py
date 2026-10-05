"""二分定位导致打印失败的 v5 批次:逐个 v5 批与 14 个 v4 批组合渲染打印。"""
from __future__ import annotations
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
sys.path.insert(0, str(ROOT / "tools"))
from render_review import build_html  # noqa: E402

V5_BATCHES = ["batch-02", "batch-05", "batch-12", "batch-14"]
OUT = ROOT / "outputs/draft-review/bisect"


def main() -> int:
    sel = json.loads((DRAFTS / "draft-selection.json").read_text(
        encoding="utf-8-sig"))
    entries = {e["batch"]: e for e in sel["entries"]}
    v4_md = {}
    for e in sel["entries"]:
        if e["batch"] not in V5_BATCHES:
            v4_md[e["batch"]] = (DRAFTS / e["report_path"]).read_text(
                encoding="utf-8-sig")
    OUT.mkdir(parents=True, exist_ok=True)
    for batch in V5_BATCHES:
        v5 = (DRAFTS / entries[batch]["report_path"]).read_text(
            encoding="utf-8-sig")
        parts = ["# bisect\n"] + list(v4_md.values()) + [v5]
        html = OUT / f"bisect-{batch}.html"
        html.write_text(build_html("\n\n".join(parts), f"bisect {batch}"),
                        encoding="utf-8", newline="\n")
        pdf = OUT / f"bisect-{batch}.pdf"
        p = Path(tempfile.mkdtemp(prefix=f"edge-bisect-{batch}-"))
        r = subprocess.run(
            [EDGE, "--headless", "--disable-gpu", "--no-first-run",
             "--allow-file-access-from-files", "--user-data-dir=" + str(p),
             f"--print-to-pdf={pdf}", "--virtual-time-budget=120000",
             html.resolve().as_uri()],
            capture_output=True, timeout=300)
        ok = pdf.exists() and pdf.read_bytes()[:4] == b"%PDF"
        print(f"{batch}: rc={r.returncode} pdf={ok and pdf.stat().st_size}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
