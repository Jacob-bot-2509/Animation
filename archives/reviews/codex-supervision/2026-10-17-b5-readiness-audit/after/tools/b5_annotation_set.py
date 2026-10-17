"""B5 标注集生成:为近重复阈值校准(calibrate.py)采样标注对。

输出 data/b5-annotation-set.json + .md:
  - 高相似候选(7/20 ≤ Jaccard < 1,取前 25 对,同题文本除外)
  - 中段样本(3/20 ≤ Jaccard < 7/20,随机 10 对)
  - 低相似对照(Jaccard < 3/20,随机 15 对)
用户逐对标注 重复/不重复/不确定,即 calibrate_threshold 的正负输入。
"""
from __future__ import annotations

import argparse
import json
import random
import uuid
from fractions import Fraction
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.b5_output import new_output_dir
from animtrain.near_dup import norm_text, shingles  # noqa: E402


def _load_problems(paths: list[Path]) -> dict[str, dict]:
    """problem_id → {problem, category, 记录数}。"""
    out: dict[str, dict] = {}
    if not paths:raise ValueError("No input records")
    for p in paths:
        data = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(data,list):raise ValueError("Expected a JSON record array")
        for rec in data:
            pid = rec.get("problem_id") or rec.get("id")
            if not isinstance(pid,str) or not pid or not isinstance(rec.get("problem"),str) or not rec["problem"].strip():
                raise ValueError("Missing problem identity or text")
            if pid in out:
                if out[pid]["problem"] != rec["problem"]:
                    raise ValueError("Conflicting text for one problem_id")
                continue
            out[pid] = {"problem": rec.get("problem", ""),
                        "category": rec.get("category", "")}
    if not out:raise ValueError("No problem records")
    return out


def _build_pairs(problems: dict[str, dict], top: int, mid: int,
                 low: int, seed: int) -> list[dict]:
    if any(type(n) is not int or n<0 for n in (top,mid,low)) or top+mid+low==0:
        raise ValueError("Sample counts must be nonnegative integers with nonzero total")
    ids = sorted(problems)
    sets = {pid: shingles(norm_text(v["problem"])) for pid, v in problems.items()}
    high, mid_, low_ = [], [], []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            left,right=sets[ids[i]],sets[ids[j]]
            union=left|right
            sim=Fraction(len(left&right),len(union)) if left and right else Fraction(0)
            # 完整题文入库供人工判重;展示层可另行截断,数据层不得截
            pair = {"a": ids[i], "b": ids[j], "jaccard": str(sim), "similarity_counts": {"intersection":len(left&right),"union":len(union)},
                    "text_a": problems[ids[i]]["problem"],
                    "text_b": problems[ids[j]]["problem"]}
            if Fraction(7,20) <= sim < 1:
                pair["stratum"]="high"
                high.append(pair)
            elif Fraction(3,20) <= sim < Fraction(7,20):
                pair["stratum"]="mid"
                mid_.append(pair)
            elif sim < Fraction(3,20):
                pair["stratum"]="low"
                low_.append(pair)
    rng = random.Random(seed)
    high.sort(key=lambda p: -Fraction(p["jaccard"]))
    return (high[:top] + rng.sample(mid_, min(mid, len(mid_)))
            + rng.sample(low_, min(low, len(low_))))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top", type=int, default=25)
    parser.add_argument("--mid", type=int, default=10)
    parser.add_argument("--low", type=int, default=15)
    parser.add_argument("--seed", type=int, default=20261004)
    parser.add_argument("--records", nargs="*", type=Path,
                        default=[ROOT / "data/v2/raw/dataset_eval.json",
                                 ROOT / "data/v2/raw/dataset_test.json"])
    parser.add_argument("--out", type=Path,
                        default=ROOT / "reviews" / "b5-candidates" / ("annotation-"+uuid.uuid4().hex))
    args = parser.parse_args(argv)
    problems = _load_problems(args.records)
    pairs = _build_pairs(problems, args.top, args.mid, args.low, args.seed)
    try:
        args.out=new_output_dir(args.out)
    except (OSError,ValueError) as error:
        parser.error(str(error))
    json_out = args.out / "b5-annotation-set.json"
    with json_out.open("x",encoding="utf-8") as output:
        output.write(json.dumps(
        {"generated_by": "tools/b5_annotation_set.py",
         "seed": args.seed, "pairs": pairs,
         "scope":"DEVELOPMENT_LABELING_CANDIDATE_NOT_INDEPENDENT_CALIBRATION"}, ensure_ascii=False, indent=2))
    md_lines = ["# B5 近重复阈值校准·标注集\n",
                "> 工具:tools/b5_annotation_set.py;输入:eval+test 全部题目文本;",
                "> 相似度=5-gram Jaccard。请在最后一列标注:重复 / 不重复 / 不确定。\n",
                "| # | Jaccard | 题目A(id) | 题目B(id) | 标注 |",
                "|---|---|---|---|---|"]
    def _md_escape(s: str) -> str:
        # 表格单元格内 | 转义为 \|,防公式中的 | 破坏列结构;JSON 保留原文
        import re
        pieces=re.split(r"(\$\$.*?\$\$|\$[^$\n]+?\$)",s,flags=re.S)
        return "".join(part if i%2 else part.replace("|",r"\|").replace("\r\n","\n").replace("\n"," ") for i,part in enumerate(pieces))

    for i, p in enumerate(pairs, 1):
        md_lines.append(
            f"| {i} | {p['jaccard']} | {_md_escape(p['text_a'])} ({p['a']}) "
            f"| {_md_escape(p['text_b'])} ({p['b']}) |  |")
    with (args.out / "b5-annotation-set.md").open("x",encoding="utf-8") as output:
        output.write("\n".join(md_lines))
    print(json.dumps({"output":str(json_out),"pairs":len(pairs),"actual_strata":{key:sum(p["stratum"]==key for p in pairs) for key in ("high","mid","low")}},ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
