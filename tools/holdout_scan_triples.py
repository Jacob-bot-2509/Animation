# -*- coding: utf-8 -*-
"""扫描每年题面/答案/解析三成分可得性,确定完整三件套年份。只读打印。"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "holdout-sources/kaoyan-math1"


def block_text(b):
    c = b.get("content", {})
    parts = []
    for key in ("title_content", "paragraph_content", "equation_content", "text_content"):
        v = c.get(key)
        if isinstance(v, list):
            for p in v:
                if isinstance(p, dict):
                    if p.get("type", "").startswith("equation"):
                        parts.append("$" + p.get("content", "") + "$")
                    else:
                        parts.append(p.get("content", ""))
                else:
                    parts.append(str(p))
    return "".join(parts)


def flow_blocks(year):
    path = SRC / f"solutions/{year}年解析/content_list_v2.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    flow = []
    for pi, page in enumerate(data):
        for b in page:
            t = block_text(b).strip()
            if t:
                flow.append((pi, b.get("bbox", [0, 0, 0, 0])[1], t))
    flow.sort(key=lambda x: (x[0], x[1]))
    return [t for _, _, t in flow]


def main() -> int:
    print(f"{'year':6} {'答案':>4} {'解':>4} {'题面n标记':>8}  结论")
    complete = []
    for year in sorted({p.name[:4] for p in (SRC / "papers").glob("*.md")
                        if re.match(r"\d{4}", p.name)}):
        cl = SRC / f"solutions/{year}年解析/content_list_v2.json"
        if not cl.exists():
            print(f"{year:6}   (无content_list)")
            continue
        blocks = flow_blocks(year)
        ans = sum(1 for t in blocks if "【答案】" in t)
        jie = sum(1 for t in blocks if "【解】" in t)
        qmarks = sum(1 for t in blocks if re.match(r"^【\s*\d{1,2}\s*】", t))
        verdict = []
        if qmarks >= 5:
            verdict.append("题面+")
        if ans >= 5:
            verdict.append("答案+")
        if jie >= 5:
            verdict.append("解析")
        ok = qmarks >= 5 and ans >= 5 and jie >= 5
        if ok:
            complete.append(year)
        print(f"{year:6} {ans:4} {jie:4} {qmarks:8}  {''.join(verdict) or '成分不全'}{'  <- 完整三件套' if ok else ''}")
    print("完整三件套年份:", complete or "无")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
