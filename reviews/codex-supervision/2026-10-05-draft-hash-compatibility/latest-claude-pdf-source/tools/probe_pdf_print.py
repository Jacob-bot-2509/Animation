"""对照实验:小页基线打印 vs 审阅稿静态页打印(有无 virtual-time-budget)。"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def print_page(html: Path, out: Path, budget: str | None) -> bool:
    args = [EDGE, "--headless", "--disable-gpu", "--no-first-run",
            "--allow-file-access-from-files",
            "--user-data-dir=C:/Users/Jacap/AppData/Local/Temp/edge-print-"
            + html.stem]
    args += [f"--print-to-pdf={out}"]
    if budget:
        args += [f"--virtual-time-budget={budget}"]
    args += [html.resolve().as_uri()]
    r = subprocess.run(args, capture_output=True, timeout=300)
    ok = out.exists() and out.stat().st_size > 0
    print(f"{html.name} budget={budget or '-'} rc={r.returncode} "
          f"pdf={'OK ' + str(out.stat().st_size) if ok else 'MISSING'}")
    return ok


def main() -> int:
    d = ROOT / "outputs/draft-review"
    small = d / "probe-small.html"
    small.write_text("<!DOCTYPE html><html><body><h1>测试</h1><p>hello</p>"
                     "</body></html>", encoding="utf-8")
    big = d / "draft-review-v4-final.static.html"
    print_page(small, d / "probe-small.pdf", None)
    print_page(small, d / "probe-small-b.pdf", "1000")
    if big.is_file():
        print_page(big, d / "probe-big-nobudget.pdf", None)
        print_page(big, d / "probe-big-b1000.pdf", "1000")
    return 0


if __name__ == "__main__":
    sys.exit(main())
