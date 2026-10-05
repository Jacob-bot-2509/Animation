"""尝试不同旗标组合打印小页,定位当前环境可行的打印方式。"""
from __future__ import annotations
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
D = ROOT / "outputs/draft-review"

VARIANTS = [
    ("base-new", ["--headless=new"]),
    ("no-gpu-disable", []),
    ("print-preview-off", ["--disable-print-preview"]),
    ("new+no-preview", ["--headless=new", "--disable-print-preview"]),
]


def main() -> int:
    small = D / "tiny.html"
    small.write_text("<html><body><h1>t</h1></body></html>",
                     encoding="utf-8")
    for tag, extra in VARIANTS:
        pdf = D / f"probe-flag-{tag}.pdf"
        p = Path(tempfile.mkdtemp(prefix=f"edge-flag-{tag}-"))
        r = subprocess.run(
            [EDGE] + extra + ["--disable-gpu", "--no-first-run",
                              "--allow-file-access-from-files",
                              "--user-data-dir=" + str(p),
                              f"--print-to-pdf={pdf}",
                              small.resolve().as_uri()],
            capture_output=True, timeout=120)
        ok = pdf.exists() and pdf.read_bytes()[:4] == b"%PDF"
        print(tag, "rc=", r.returncode, "pdf=", ok and pdf.stat().st_size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
