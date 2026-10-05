"""在渲染 DOM 中定位 MathJax 错误节点及其数学原文上下文。"""
from __future__ import annotations
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def main() -> int:
    html = ROOT / "outputs/draft-review/draft-review-selected-v5.html"
    profile = Path(tempfile.mkdtemp(prefix="edge-err-locate-"))
    r = subprocess.run(
        [EDGE, "--headless", "--disable-gpu", "--no-first-run",
         "--allow-file-access-from-files",
         "--user-data-dir=" + str(profile),
         "--dump-dom", "--virtual-time-budget=240000", html.resolve().as_uri()],
        capture_output=True, timeout=300)
    dom = r.stdout.decode("utf-8", "replace")
    Path(ROOT / "outputs/draft-review/err-dom.html").write_text(
        dom, encoding="utf-8", newline="\n")
    # 找 merror 节点,回溯最近的 span.math 原文
    for m in re.finditer(r'data-mml-node="merror"[^>]*>(.*?)</mjx-merror>',
                         dom, re.S):
        start = m.start()
        back = dom.rfind('<span class="math">', 0, start)
        fwd = dom.find('</span>', start)
        src = dom[back + len('<span class="math">'):start]
        src = src[src.rfind("$"):]
        err = re.sub(r"<[^>]+>", "", m.group(1))[:120]
        print("错误内容:", err)
        print("数学原文:", src[:200])
        print("---")
    return 0


if __name__ == "__main__":
    sys.exit(main())
