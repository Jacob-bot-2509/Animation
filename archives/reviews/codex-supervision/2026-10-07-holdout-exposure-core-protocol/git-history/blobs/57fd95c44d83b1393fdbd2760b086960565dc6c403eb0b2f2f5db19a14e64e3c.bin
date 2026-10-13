"""B5 校准执行:读已标注对照集 → calibrate_threshold + 权衡表 → 报告。

输入 data/b5-annotation-set/b5-annotation-set.json(带 label 字段);
输出 data/b5-calibration-report.json + .md(不伪造:目标不达标即如实报
UNCALIBRATED,并给出交错区分析与权衡阈值建议)。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.calibrate import calibrate_threshold, evaluate_at  # noqa: E402


def _load_problem_texts(paths: list[Path]) -> dict[str, str]:
    out: dict[str, str] = {}
    for p in paths:
        data = json.loads(p.read_text(encoding="utf-8"))
        for rec in (data if isinstance(data, list) else []):
            pid = rec.get("problem_id") or rec.get("id")
            out.setdefault(pid, rec.get("problem", ""))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--annotation", type=Path,
                    default=ROOT / "data" / "b5-annotation-set"
                    / "b5-annotation-set.json")
    ap.add_argument("--records", nargs="*", type=Path,
                    default=[ROOT / "data/v2/eval/dataset_eval.json",
                             ROOT / "data/v2/test/dataset_test.json"])
    ap.add_argument("--out", type=Path,
                    default=ROOT / "data" / "b5-calibration-report")
    args = ap.parse_args(argv)
    annot = json.loads(args.annotation.read_text(encoding="utf-8"))
    texts = _load_problem_texts(args.records)
    pos_queries: list[str] = []
    neg_queries: list[str] = []
    labeled = 0
    uncertain = 0
    for i, p in enumerate(annot["pairs"], 1):
        label = p.get("label")
        if label == "重复":
            pos_queries.append(p["text_a"])
            pos_queries.append(p["text_b"])
            labeled += 1
        elif label == "不重复":
            neg_queries.append(p["text_a"])
            neg_queries.append(p["text_b"])
            labeled += 1
        else:
            uncertain += 1
    pool = list(texts.values())
    report = calibrate_threshold(pool, pos_queries, neg_queries)
    # 权衡表:细网格扫 recall/fpr,并找 F1 最优权衡点(报告用,不改判定口径)
    tradeoff = []
    best_f1 = None
    t = 0.30
    while t <= 0.80 + 1e-9:
        r = evaluate_at(pool, pos_queries, neg_queries, t)
        if r["precision"] and r["recall"]:
            f1 = round(2 * r["precision"] * r["recall"]
                       / (r["precision"] + r["recall"]), 4)
            if best_f1 is None or f1 > best_f1["f1"]:
                best_f1 = {**r, "f1": f1}
        tradeoff.append(r)
        t = round(t + 0.05, 6)
    # 交错区分析:按 Jaccard 升序列出 0.40-0.65 区间的重复/不重复对
    interleave = sorted(
        [{"jaccard": p["jaccard"], "label": p.get("label"),
          "a": p["a"], "b": p["b"],
          "text_a": p["text_a"][:48], "text_b": p["text_b"][:48]}
         for p in annot["pairs"]
         if p.get("label") in ("重复", "不重复") and 0.40 <= p["jaccard"] <= 0.65],
        key=lambda x: x["jaccard"])
    out = {"annotated_pairs": labeled, "uncertain_pairs": uncertain,
           "pos_queries": len(pos_queries), "neg_queries": len(neg_queries),
           "calibration": {"threshold": report.threshold,
                           "calibrated": report.calibrated,
                           "tp": report.tp, "fp": report.fp,
                           "fn": report.fn, "tn": report.tn,
                           "precision": report.precision,
                           "recall": report.recall,
                           "fpr": report.fpr, "fnr": report.fnr,
                           "note": report.note},
           "tradeoff": tradeoff, "best_f1_tradeoff": best_f1,
           "interleave_zone": interleave}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "b5-calibration-report.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    md = ["# B5 近重复阈值校准报告\n",
          f"- 标注对:{labeled}(重复 {len(pos_queries) // 2} 对 / "
          f"不重复 {len(neg_queries) // 2} 对),不确定 {uncertain} 对不参与",
          f"- 默认目标:recall≥0.95 且 fpr≤0.01",
          f"- 校准结论:**{'已校准,阈值=' + str(report.threshold)
          if report.calibrated else 'UNCALIBRATED —— ' + report.note}**\n",
          "## 权衡表(细网格)\n",
          "| 阈值 | TP | FP | FN | TN | precision | recall | fpr |",
          "|---|---|---|---|---|---|---|---|"]
    for r in tradeoff:
        md.append(f"| {r['threshold']} | {r['tp']} | {r['fp']} | {r['fn']} "
                  f"| {r['tn']} | {r['precision']} | {r['recall']} | {r['fpr']} |")
    if best_f1:
        md.append(f"\nF1 最优权衡点:阈值 {best_f1['threshold']}"
                  f"(precision={best_f1['precision']},"
                  f"recall={best_f1['recall']},fpr={best_f1['fpr']})"
                  "——仅供参考,非验收口径。\n")
    md.append("## 交错区(0.40~0.65,升序)\n")
    md.append("| Jaccard | 标注 | 题目A(id) | 题目B(id) |")
    md.append("|---|---|---|---|")
    for it in interleave:
        md.append(f"| {it['jaccard']} | {it['label']} | "
                  f"{it['text_a']} ({it['a']}) | {it['text_b']} ({it['b']}) |")
    (args.out / "b5-calibration-report.md").write_text(
        "\n".join(md), encoding="utf-8")
    print(json.dumps({"calibrated": report.calibrated,
                      "threshold": report.threshold,
                      "recall": report.recall, "fpr": report.fpr,
                      "best_f1": best_f1["threshold"] if best_f1 else None},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
