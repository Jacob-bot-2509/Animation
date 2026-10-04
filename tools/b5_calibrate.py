"""B5 校准执行 v2:直接评估已标注对的 pairwise Jaccard(应 msg_371)。

v1 缺陷:把每个 pair 拆成两个 query 查完整 pool(含自身)→ max_sim 恒 1,
权衡表自污染。v2 改为:每对用其采样的 pairwise Jaccard 直接对阈值判
TP/FP/FN/TN,网格扫描严格目标(recall≥0.95 且 fpr≤0.01),不达标如实
UNCALIBRATED;报告含完整分子/分母/精确值、交错区完整题文(MD 单元格
转义 |,不再截断)。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _md_escape(s: str) -> str:
    return s.replace("|", "\\|")


def evaluate_pairs(pairs: list[dict], threshold: float) -> dict:
    """直接 pairwise:每对以其自身 Jaccard 对阈值判定。"""
    tp = sum(1 for p in pairs if p["label"] == "重复" and p["jaccard"] >= threshold)
    fn = sum(1 for p in pairs if p["label"] == "重复" and p["jaccard"] < threshold)
    fp = sum(1 for p in pairs if p["label"] == "不重复" and p["jaccard"] >= threshold)
    tn = sum(1 for p in pairs if p["label"] == "不重复" and p["jaccard"] < threshold)
    pos, neg = tp + fn, fp + tn

    def ratio(a: int, b: int):
        return round(a / b, 4) if b else None
    return {"threshold": threshold, "tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "pos": pos, "neg": neg,
            "precision": ratio(tp, tp + fp), "recall": ratio(tp, pos),
            "fpr": ratio(fp, neg), "fnr": ratio(fn, pos)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--annotation", type=Path,
                    default=ROOT / "data" / "b5-annotation-set"
                    / "b5-annotation-set.json")
    ap.add_argument("--out", type=Path,
                    default=ROOT / "data" / "b5-calibration-report")
    args = ap.parse_args(argv)
    annot = json.loads(args.annotation.read_text(encoding="utf-8"))
    labeled = [p for p in annot["pairs"]
               if p.get("label") in ("重复", "不重复")]
    uncertain = [p for p in annot["pairs"] if p.get("label") == "不确定"]
    # 严格目标网格(与项目 calibrate.py 同口径)
    grid = []
    best = None
    t = 0.30
    while t <= 0.80 + 1e-9:
        r = evaluate_pairs(labeled, t)
        grid.append(r)
        if (r["recall"] is not None and r["fpr"] is not None
                and r["recall"] >= 0.95 and r["fpr"] <= 0.01):
            best = r
            break
        t = round(t + 0.05, 6)
    interleave = sorted(
        [{"jaccard": p["jaccard"], "label": p["label"],
          "a": p["a"], "b": p["b"],
          "text_a": p["text_a"], "text_b": p["text_b"]}
         for p in labeled if 0.40 <= p["jaccard"] <= 0.65],
        key=lambda x: x["jaccard"])
    out = {"annotated_pairs": len(labeled),
           "pos_pairs": sum(1 for p in labeled if p["label"] == "重复"),
           "neg_pairs": sum(1 for p in labeled if p["label"] == "不重复"),
           "uncertain_pairs": len(uncertain),
           "evaluation": "pairwise(每对以其自身 Jaccard 对阈值判定,"
                         "无 query-vs-pool 自污染)",
           "calibration": {
               "threshold": best["threshold"] if best else 0.0,
               "calibrated": best is not None,
               "tp": best["tp"] if best else 0,
               "fp": best["fp"] if best else 0,
               "fn": best["fn"] if best else 0,
               "tn": best["tn"] if best else 0,
               "note": (f"网格扫描选定 {best['threshold']}(recall={best['recall']},"
                        f"fpr={best['fpr']})"
                        if best else
                        "网格内无阈值同时满足 recall≥0.95 且 fpr≤0.01——"
                        "对照集或方法需检查,当前阈值仍 UNCALIBRATED")},
           "grid": grid, "interleave_zone": interleave}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "b5-calibration-report.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    md = ["# B5 近重复阈值校准报告 v2(pairwise 评估)\n",
          f"- 标注对:{len(labeled)}(重复 {out['pos_pairs']} 对 / "
          f"不重复 {out['neg_pairs']} 对),不确定 {len(uncertain)} 对不参与",
          "- 评估口径:每对以其自身 pairwise Jaccard 对阈值判定"
          "(修复 v1 的 query-vs-pool 自污染)",
          f"- 校准结论:**{'已校准,阈值=' + str(out['calibration']['threshold'])
          if out['calibration']['calibrated']
          else 'UNCALIBRATED —— ' + out['calibration']['note']}**\n",
          "## 网格表(0.30~0.80,步长 0.05)\n",
          "| 阈值 | TP | FP | FN | TN | precision | recall | fpr |",
          "|---|---|---|---|---|---|---|---|"]
    for r in grid:
        md.append(f"| {r['threshold']} | {r['tp']} | {r['fp']} | {r['fn']} "
                  f"| {r['tn']} | {r['precision']} | {r['recall']} | {r['fpr']} |")
    md.append("\n## 交错区(0.40~0.65,升序,完整题文)\n")
    md.append("| Jaccard | 标注 | 题目A(id) | 题目B(id) |")
    md.append("|---|---|---|---|")
    for it in interleave:
        md.append(f"| {it['jaccard']} | {it['label']} | "
                  f"{_md_escape(it['text_a'])} ({it['a']}) | "
                  f"{_md_escape(it['text_b'])} ({it['b']}) |")
    (args.out / "b5-calibration-report.md").write_text(
        "\n".join(md), encoding="utf-8")
    print(json.dumps({"calibrated": out["calibration"]["calibrated"],
                      "threshold": out["calibration"]["threshold"],
                      "note": out["calibration"]["note"][:100]},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
