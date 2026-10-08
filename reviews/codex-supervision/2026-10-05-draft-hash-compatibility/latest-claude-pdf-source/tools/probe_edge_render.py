"""探测 Edge headless 对审阅稿 HTML 的 MathJax 渲染状态(独立临时 profile)。"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def main() -> int:
    html = (ROOT / "outputs/draft-review/draft-review-v4-final.html")
    for budget in (30000, 240000):
        r = subprocess.run(
            [EDGE, "--headless", "--disable-gpu", "--no-first-run",
             "--allow-file-access-from-files",
             "--user-data-dir=C:/Users/Jacap/AppData/Local/Temp/edge-probe-b" + str(budget),
             "--dump-dom", f"--virtual-time-budget={budget}", html.as_uri()],
            capture_output=True, timeout=300)
        dom = r.stdout.decode("utf-8", "replace")
        print(f"budget={budget} rc={r.returncode} dom_len={len(dom)} "
              f"spans={dom.count('class=\"math\"')} mjx={dom.count('mjx-container')} "
              f"MJDONE={'MJDONE' in dom}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
