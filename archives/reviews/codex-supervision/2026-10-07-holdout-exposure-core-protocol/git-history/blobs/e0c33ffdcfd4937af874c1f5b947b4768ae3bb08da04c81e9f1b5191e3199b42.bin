"""B5 标注集生成:为近重复阈值校准(calibrate.py)采样标注对。

输出 data/b5-annotation-set.json + .md:
  - 高相似候选(0.35 ≤ Jaccard < 1.0,取前 25 对,同题文本除外)
  - 中段样本(0.15 ≤ Jaccard < 0.35,随机 10 对)
  - 低相似对照(Jaccard < 0.15,随机 15 对)
用户逐对标注 重复/不重复/不确定,即 calibrate_threshold 的正负输入。
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.near_dup import jaccard, norm_text, shingles  # noqa: E402


def _load_problems(paths: list[Path]) -> dict[str, dict]:
    """problem_id → {problem, category, 记录数}。"""
    out: dict[str, dict] = {}
    for p in paths:
        data = json.loads(p.read_text(encoding="utf-8"))
        for rec in (data if isinstance(data, list) else []):
            pid = rec.get("problem_id") or rec.get("id")
            if pid in out:
                continue
            out[pid] = {"problem": rec.get("problem", ""),
                        "category": rec.get("category", "")}
    return out


def _build_pairs(problems: dict[str, dict], top: int, mid: int,
                 low: int, seed: int) -> list[dict]:
    ids = sorted(problems)
    sets = {pid: shingles(norm_text(v["problem"])) for pid, v in problems.items()}
    high, mid_, low_ = [], [], []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            sim = jaccard(sets[ids[i]], sets[ids[j]])
            pair = {"a": ids[i], "b": ids[j], "jaccard": round(sim, 4),
                    "text_a": problems[ids[i]]["problem"][:80],
                    "text_b": problems[ids[j]]["problem"][:80]}
            if 0.35 <= sim < 1.0:
                high.append(pair)
            elif 0.15 <= sim < 0.35:
                mid_.append(pair)
            elif sim < 0.15:
                low_.append(pair)
    rng = random.Random(seed)
    high.sort(key=lambda p: -p["jaccard"])
    return (high[:top] + rng.sample(mid_, min(mid, len(mid_)))
            + rng.sample(low_, min(low, len(low_))))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top", type=int, default=25)
    parser.add_argument("--mid", type=int, default=10)
    parser.add_argument("--low", type=int, default=15)
    parser.add_argument("--seed", type=int, default=20261004)
    parser.add_argument("--records", nargs="*", type=Path,
                        default=[ROOT / "data/v2/eval/dataset_eval.json",
                                 ROOT / "data/v2/test/dataset_test.json"])
    parser.add_argument("--out", type=Path,
                        default=ROOT / "data" / "b5-annotation-set")
    args = parser.parse_args(argv)
    problems = _load_problems(args.records)
    pairs = _build_pairs(problems, args.top, args.mid, args.low, args.seed)
    args.out.mkdir(parents=True, exist_ok=True)
    json_out = args.out / "b5-annotation-set.json"
    json_out.write_text(json.dumps(
        {"generated_by": "tools/b5_annotation_set.py",
         "seed": args.seed, "pairs": pairs}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    md_lines = ["# B5 近重复阈值校准·标注集\n",
                "> 工具:tools/b5_annotation_set.py;输入:eval+test 全部题目文本;",
                "> 相似度=5-gram Jaccard。请在最后一列标注:重复 / 不重复 / 不确定。\n",
                "| # | Jaccard | 题目A(id) | 题目B(id) | 标注 |",
                "|---|---|---|---|---|"]
    for i, p in enumerate(pairs, 1):
        md_lines.append(
            f"| {i} | {p['jaccard']} | {p['text_a']} ({p['a']}) "
            f"| {p['text_b']} ({p['b']}) |  |")
    (args.out / "b5-annotation-set.md").write_text(
        "\n".join(md_lines), encoding="utf-8")
    print(f"标注集已生成:{json_out}({len(pairs)} 对:高{args.top}/中{args.mid}/低{args.low})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
