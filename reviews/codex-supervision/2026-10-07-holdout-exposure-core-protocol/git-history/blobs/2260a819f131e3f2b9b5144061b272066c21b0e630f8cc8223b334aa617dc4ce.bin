"""B5 校准 v3:本质考点规则(模块+题型)主判定;5-gram 精确分数网格仅作对照。

历史:
- v1 缺陷:每对拆两个 query 查完整 pool(含自身)→ max_sim 恒 1,
  权衡表自污染(应 msg_371)。
- v2:改 pairwise 直接评估(5-gram Jaccard),自污染修复;严格目标
  (recall≥19/20 且 fpr≤1/100)网格内无解,如实 UNCALIBRATED——文字相似度
  本身区分不了用户判重标准(应 msg_376 独立复验一致)。
- v3(应用户裁决 2026-10-04):用户明确判重依据=题目**本质考点**,粒度=
  模块+题型;8 处规则冲突对经用户逐项确认按规则改判(label_prev 保留原
  标注)。主判定=考点签名 (category, 题型) 相等,题型由题文动词分类、
  sub_category 兜底;考点 token Jaccard ∈ {0, 1/3, 1},离散网格扫严格
  目标。报告含精确分数(分母为 0 显示"未定义",未选中阈值用 null,应监督
  报告第 4 项)、8 处裁决表、全 48 对证据表、不确定对预测;结论边界如实
  声明(仅该 48 对分层样本成立,不推断总体性能)。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.near_dup import shingles  # noqa: E402

MIN_RECALL = Fraction(19, 20)
MAX_FPR = Fraction(1, 100)
DATASETS = (("data/v2/eval/dataset_eval.jsonl", "problem_id"),
            ("data/v2/test/dataset_test.jsonl", "id"),
            ("data/v1/test/dataset_test.jsonl", "id"))


def _md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\r\n", "\n").replace("\n", " ")


def _load_records() -> dict[str, dict]:
    """问题 id → 结构化记录;v2 优先(v1 仅补 v2 缺失 id),不互相覆盖。"""
    out: dict[str, dict] = {}
    for path, key in DATASETS:
        for line in (ROOT / path).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            k = rec.get(key)
            if k is not None and k not in out:
                out[k] = rec
    return out


def classify_kp(rec: dict) -> str:
    """题型分类(考点签名的题型分量):题文动词优先,sub_category 兜底。"""
    text = rec.get("problem", "")
    sub = rec.get("sub_category", "")
    if "极限" in text or r"\lim" in text or "lim " in text:
        return "极限计算"
    if "不定积分" in text:
        return "不定积分"
    if "反常积分" in text or "反常积分" in sub:
        return "反常积分"
    if "行列式" in text:
        return "三对角行列式" if "三对角" in text else "行列式计算"
    if "特征值" in text or "对角化" in text:
        return "特征值对角化"
    if "微分方程" in text:
        return "微分方程组" if "微分方程组" in text else "常微分方程"
    if "级数" in text or "级数" in sub:
        if "收敛" in text or "敛散" in text or "敛散" in sub or "判别" in sub:
            return "级数敛散"
        return "级数求和"
    if not isinstance(sub, str) or not sub.strip():
        raise ValueError("题型无法识别且缺少 sub_category，不能把缺失值当成共同考点")
    return f"其他[{sub}]"


def kp_signature(rec: dict) -> tuple[str, str]:
    if not isinstance(rec.get("category"), str) or not rec["category"].strip():
        raise ValueError("结构化题目缺少模块 category")
    if not isinstance(rec.get("problem"), str) or not rec["problem"].strip():
        raise ValueError("结构化题目缺少完整题文 problem")
    return (rec["category"], classify_kp(rec))


def kp_tokens(rec: dict) -> set[tuple[str, str]]:
    category, kind = kp_signature(rec)
    return {("category", category), ("kind", kind)}


def kp_jaccard(a: set[tuple[str, str]], b: set[tuple[str, str]]) -> Fraction:
    union = a | b
    return Fraction(len(a & b), len(union)) if union else Fraction(0)


def _prepare_pair(pair: dict) -> dict:
    if pair.get("label") not in ("重复", "不重复", "不确定"):
        raise ValueError("每个标注对必须标为重复、不重复或不确定")
    if not all(isinstance(pair.get(key), str) for key in ("text_a", "text_b")):
        raise ValueError("标注对必须包含完整题文 text_a/text_b")
    if not all(isinstance(pair.get(key), str) and pair[key] for key in ("a", "b")):
        raise ValueError("标注对必须包含非空题目 id a/b")
    a, b = shingles(pair["text_a"]), shingles(pair["text_b"])
    intersection, union = len(a & b), len(a | b)
    score = Fraction(intersection, union) if a and b else Fraction(0)
    return {**pair, "jaccard": str(score),
            "similarity_counts": {"intersection": intersection, "union": union}}


def _ratio(numerator: int, denominator: int) -> str | None:
    return str(Fraction(numerator, denominator)) if denominator else None


def _evaluate(pairs: list[dict], threshold: Fraction, key: str) -> dict:
    tp = fp = fn = tn = 0
    for pair in pairs:
        positive = Fraction(pair[key]) >= threshold
        if pair["label"] == "重复":
            tp += positive
            fn += not positive
        elif pair["label"] == "不重复":
            fp += positive
            tn += not positive
    counts = {"precision": (tp, tp + fp), "recall": (tp, tp + fn),
              "fpr": (fp, fp + tn), "fnr": (fn, fn + tp)}
    return {"threshold": str(threshold), "tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "pos": tp + fn, "neg": fp + tn,
            **{name: _ratio(n, d) for name, (n, d) in counts.items()},
            "metric_counts": {name: {"numerator": n, "denominator": d}
                              for name, (n, d) in counts.items()}}


def build_report(annotation: dict, records: dict[str, dict] | None = None) -> dict:
    prepared = [_prepare_pair(pair) for pair in annotation["pairs"]]
    labeled = [pair for pair in prepared if pair["label"] != "不确定"]
    uncertain = [pair for pair in prepared if pair["label"] == "不确定"]
    records = _load_records() if records is None else records
    missing = sorted({q for pair in prepared for q in (pair["a"], pair["b"])
                      if q not in records})
    if missing:
        raise ValueError(f"标注对引用的问题无结构化记录: {missing}")
    # 每对附字段带名的考点token，模块和题型不得互相混淆。
    for pair in labeled + uncertain:
        for side in ("a", "b"):
            rec = records[pair[side]]
            kp_signature(rec)
            if pair["text_" + side] != rec["problem"]:
                raise ValueError(f"标注题文与结构化记录不一致: {pair[side]}")
        ta, tb = kp_tokens(records[pair["a"]]), kp_tokens(records[pair["b"]])
        pair["kp_a"] = " ".join(kp_signature(records[pair["a"]]))
        pair["kp_b"] = " ".join(kp_signature(records[pair["b"]]))
        pair["kp_j"] = str(kp_jaccard(ta, tb))
        pair["prediction"] = "重复" if pair["kp_j"] == "1" else "不重复"
    mismatches = [{"a": pair["a"], "b": pair["b"], "label": pair["label"],
                   "prediction": pair["prediction"]}
                  for pair in labeled if pair["prediction"] != pair["label"]]
    # 裁决表条目补 reason(来自各对 revise_reason,缺省为空)
    revision = dict(annotation.get("label_revision", {}))
    changed = []
    for change in revision.get("changed_pairs", []):
        change = dict(change)
        if not change.get("reason"):
            hit = [p for p in annotation["pairs"]
                   if {p.get("a"), p.get("b")} == {change.get("a"), change.get("b")}]
            change["reason"] = hit[0].get("revise_reason", "") if hit else ""
        changed.append(change)
    revision["changed_pairs"] = changed
    # 5-gram 网格(3/10~4/5,步长 1/20)仅作对照,v2 已证其不可校准
    grid_5gram = [_evaluate(labeled, Fraction(i, 20), "jaccard")
                  for i in range(6, 17)]
    # 考点网格:离散取值 0 / 1/3 / 1,升序取首个达标阈值
    grid_kp = [_evaluate(labeled, t, "kp_j")
               for t in (Fraction(0), Fraction(1, 3), Fraction(1))]
    # 主规则固定为签名相等(kp_j=1)。其他网格行仅作诊断，
    # 不能选低阈值来宣称不同题型的同模块题也满足签名相等。
    best = next((row for row in grid_kp
                 if row["threshold"] == "1"
                 and row["recall"] is not None and row["fpr"] is not None
                 and Fraction(row["recall"]) >= MIN_RECALL
                 and Fraction(row["fpr"]) <= MAX_FPR), None)
    note = (f"考点网格选定阈值 {best['threshold']}(考点签名完全一致),"
            f"召回率={best['recall']},误报率={best['fpr']}" if best else
            "签名相等主规则未同时满足召回率≥19/20且误报率≤1/100;"
            "没有选定阈值,仍为 UNCALIBRATED")
    calibration = {"calibrated": best is not None, "note": note,
                   **{key: best[key] if best else None
                      for key in ("threshold", "tp", "fp", "fn", "tn",
                                  "precision", "recall", "fpr", "fnr")}}
    return {"schema": 3,
            "rule": {"criterion": "本质考点 = (category, 题型)",
                     "taxonomy": "题型由题文动词分类,sub_category 兜底",
                     "approved_by_user": "2026-10-04"},
            "label_revision": revision,
            "annotated_pairs": len(labeled),
            "pos_pairs": sum(pair["label"] == "重复" for pair in labeled),
            "neg_pairs": sum(pair["label"] == "不重复" for pair in labeled),
            "uncertain_pairs": len(uncertain),
            "evaluation": "pairwise 考点签名相等判定(无自污染);"
                          "5-gram 网格仅对照不参与结论",
            "targets": {"min_recall": str(MIN_RECALL), "max_fpr": str(MAX_FPR)},
            "sample_scope": "仅评估当前标注样本;分层采样不构成总体性能保证",
            "calibration": calibration,
            "grid_kp": grid_kp,
            "grid_5gram_contrast": grid_5gram,
            "pairs": [{"a": pair["a"], "b": pair["b"], "j5": pair["jaccard"],
                       "similarity_counts": pair["similarity_counts"],
                       "kp_a": pair["kp_a"], "kp_b": pair["kp_b"],
                       "kp_j": pair["kp_j"], "label": pair["label"],
                       "prediction": pair["prediction"],
                       "match": pair["prediction"] == pair["label"],
                       "text_a": pair["text_a"], "text_b": pair["text_b"]}
                      for pair in labeled],
            "uncertain": [{"a": pair["a"], "b": pair["b"],
                           "kp_a": pair["kp_a"], "kp_b": pair["kp_b"],
                           "prediction": pair["prediction"],
                           "text_a": pair["text_a"], "text_b": pair["text_b"]}
                          for pair in uncertain],
            "mismatches": mismatches}


def render_markdown(report: dict) -> str:
    display = lambda value: "未定义" if value is None else str(value)
    cal = report["calibration"]
    lines = ["# B5 近重复阈值校准报告 v3(本质考点规则)", "",
             "- 判重依据:用户确认(2026-10-04)= 题目**本质考点**,粒度=模块+题型",
             "- 考点签名:(category, 题型);题型由题文动词分类,结构化字段兜底",
             f"- 有效标注:{report['annotated_pairs']} 对,其中重复 "
             f"{report['pos_pairs']} 对、不重复 {report['neg_pairs']} 对;"
             f"不确定 {report['uncertain_pairs']} 对排除。",
             "- 目标:召回率≥19/20,误报率≤1/100。",
             f"- 结论:**{cal['note']}**"
             + (f"(TP {cal['tp']},FP {cal['fp']},FN {cal['fn']},TN {cal['tn']})"
                if cal["calibrated"] else ""),
             f"- 范围:{report['sample_scope']}。", "",
             "## 考点网格(离散取值 0 / 1/3 / 1)", "",
             "| 阈值 | TP | FP | FN | TN | 精确率 | 召回率 | 误报率 |",
             "|---|---|---|---|---|---|---|---|"]
    for row in report["grid_kp"]:
        lines.append("| " + " | ".join(display(row[key]) for key in
                     ("threshold", "tp", "fp", "fn", "tn",
                      "precision", "recall", "fpr")) + " |")
    lines += ["", "精确率=TP/(TP+FP),召回率=TP/(TP+FN),"
              "误报率=FP/(FP+TN)。分母为零时显示“未定义”。",
              "", "## 全对证据(48 对;J5 为文字 5-gram Jaccard,仅对照)", "",
              "| J5(文字) | 标注 | 题目A(考点) | 题目B(考点) |",
              "|---|---|---|---|"]
    for pair in report["pairs"]:
        lines.append(f"| {pair['j5']} | {pair['label']} | "
                     f"{_md_escape(pair['text_a'])} ({pair['a']};考点:{pair['kp_a']}) | "
                     f"{_md_escape(pair['text_b'])} ({pair['b']};考点:{pair['kp_b']}) |")
    if report["label_revision"].get("changed_pairs"):
        lines += ["", "## 标注裁决(规则冲突对,用户逐项确认按规则改判)", "",
                  "| 对 | 原标注 | 改判 | 理由 |", "|---|---|---|---|"]
        for change in report["label_revision"]["changed_pairs"]:
            lines.append(f"| {change['a']} × {change['b']} | {change['from']} "
                         f"| {change['to']} | {_md_escape(change['reason'])} |")
    lines += ["", "## 5-gram 对照网格(3/10 至 4/5,步长 1/20)", "",
              "v2 已证文字 5-gram 区分不了标注(应 msg_376 独立复验一致),"
              "此处仅作对照,不参与校准结论。", "",
              "| 阈值 | TP | FP | FN | TN | 精确率 | 召回率 | 误报率 |",
              "|---|---|---|---|---|---|---|---|"]
    for row in report["grid_5gram_contrast"]:
        lines.append("| " + " | ".join(display(row[key]) for key in
                     ("threshold", "tp", "fp", "fn", "tn",
                      "precision", "recall", "fpr")) + " |")
    if report["uncertain"]:
        lines += ["", "## 不确定对(不参与校准,仅规则预测)", "",
                  "| 题目A(考点) | 题目B(考点) | 规则预测 |",
                  "|---|---|---|"]
        for pair in report["uncertain"]:
            lines.append(f"| {_md_escape(pair['text_a'])} "
                         f"({pair['a']};考点:{pair['kp_a']}) "
                         f"| {_md_escape(pair['text_b'])} "
                         f"({pair['b']};考点:{pair['kp_b']}) "
                         f"| {pair['prediction']} |")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--annotation", type=Path,
                    default=ROOT / "data/b5-annotation-set/b5-annotation-set.json")
    ap.add_argument("--out", type=Path, default=ROOT / "data/b5-calibration-report")
    args = ap.parse_args(argv)
    raw = args.annotation.read_bytes()
    try:
        report = build_report(json.loads(raw))
    except (ValueError, KeyError, TypeError) as error:
        ap.error(str(error))
    report["annotation_sha256"] = hashlib.sha256(raw).hexdigest()
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "b5-calibration-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.out / "b5-calibration-report.md").write_text(
        render_markdown(report), encoding="utf-8")
    print(json.dumps({"calibrated": report["calibration"]["calibrated"],
                      "note": report["calibration"]["note"],
                      "mismatches": report["mismatches"]},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
