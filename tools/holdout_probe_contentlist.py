# -*- coding: utf-8 -*-
"""探测 content_list_v2.json 的分段结构:重建阅读序文本流,
统计【答案】/【解】锚点数,并看锚点间段是否含题面。只读打印。"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "holdout-sources/kaoyan-math1/solutions"


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
        elif isinstance(v, str):
            parts.append(v)
    return "".join(parts)


def read_flow(year):
    path = SRC / f"{year}年解析/content_list_v2.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    flow = []
    for pi, page in enumerate(data):
        for b in page:
            t = block_text(b).strip()
            if t:
                flow.append((pi, b.get("bbox", [0, 0, 0, 0])[1], b.get("type"), t))
    flow.sort(key=lambda x: (x[0], x[1]))
    return flow


def main() -> int:
    for year in ("1987", "2024"):
        flow = read_flow(year)
        ans_idx = [i for i, x in enumerate(flow) if "【答案】" in x[3]]
        jie_idx = [i for i, x in enumerate(flow) if x[3].startswith("【解】") or x[3] == "【解】"]
        print(f"=== {year}: blocks={len(flow)} 答案锚={len(ans_idx)} 解锚={len(jie_idx)}")
        # 看前两个答案锚之间的段结构
        for k in range(min(2, len(ans_idx) - 1)):
            seg = flow[ans_idx[k]:ans_idx[k + 1]]
            print(f"  段{k+1} ({len(seg)}块):")
            for x in seg[:6]:
                print(f"    [{x[2]}] {x[3][:70]}")
            print("    ...")
        # 首段与末段
        print("  首段(题头):")
        for x in flow[:6]:
            print(f"    [{x[2]}] {x[3][:70]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
