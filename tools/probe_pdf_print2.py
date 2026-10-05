"""复刻 render_review 打印调用的对照实验(mkdtemp profile + 同名目标)。"""
from __future__ import annotations
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def main() -> int:
    d = ROOT / "outputs/draft-review"
    static = d / "draft-review-v4-final.static.html"
    pdf = d / "draft-review-v4-final.pdf"
    profile = Path(tempfile.mkdtemp(prefix="edge-headless-"))
    args = [EDGE, "--headless", "--disable-gpu", "--no-first-run",
            "--allow-file-access-from-files",
            "--user-data-dir=" + str(profile),
            f"--print-to-pdf={pdf}", "--virtual-time-budget=1000",
            static.resolve().as_uri()]
    r = subprocess.run(args, capture_output=True, timeout=300)
    print("rc:", r.returncode, "| pdf exists:",
          pdf.exists() and pdf.stat().st_size)
    # 全盘找漏网 pdf
    hits = list(ROOT.rglob("draft-review-v4-final.pdf"))
    print("全盘命中:", [str(h) for h in hits])
    return 0


if __name__ == "__main__":
    sys.exit(main())
