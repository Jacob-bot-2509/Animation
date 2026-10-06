# -*- coding: utf-8 -*-
"""预留题池与项目全部数据的去重核对:
归一化(去空白/统一全半角/去LaTeX间距)后比对 problem+answer 对。
只读打印,不产出文件。"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def norm(text: str) -> str:
    t = str(text)
    t = t.replace(" ", "").replace("　", "").replace("\n", "")
    t = re.sub(r"\\,|\\;|\\!|\\:", "", t)
    t = t.replace("（", "(").replace("）", ")")
    t = t.replace("，", ",").replace("。", ".")
    return t


def load_kaoyan():
    recs = [json.loads(l) for l in
            (ROOT / "holdout-sources/extracted/kaoyan-triples.jsonl")
            .read_text(encoding="utf-8").splitlines()]
    return {(norm(r["problem"]), norm(r["answer"])): r["id"] for r in recs}


def load_project_pairs():
    pairs = set()
    paths = list((ROOT / "data/v2/train/leakage-isolated-v3-2026-10-05").glob("*.jsonl"))
    paths += list((ROOT / "data/v2").glob("eval/*.jsonl")) + list((ROOT / "data/v2").glob("test/*.jsonl"))
    for p in paths:
        try:
            for line in p.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                r = json.loads(line)
                if "problem" in r and "answer" in r:
                    pairs.add((norm(r["problem"]), norm(r["answer"])))
        except (json.JSONDecodeError, OSError):
            continue
    return pairs


def main() -> int:
    kaoyan = load_kaoyan()
    project = load_project_pairs()
    print("kaoyan triples:", len(kaoyan))
    print("project problem+answer pairs:", len(project))
    overlap = [kid for pair, kid in kaoyan.items() if pair in project]
    print("exact normalized overlap:", len(overlap), overlap[:10])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
