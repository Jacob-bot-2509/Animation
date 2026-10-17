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
import re
import sys
import uuid
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.b5_output import new_output_dir
from animtrain.near_dup import shingles  # noqa: E402
from animtrain.kp_rule import (  # noqa: E402
    classify_kp, kp_jaccard, kp_signature, kp_tokens)

MIN_RECALL = Fraction(19, 20)
MAX_FPR = Fraction(1, 100)
DATASETS = (("data/v2/eval/dataset_eval.jsonl", "problem_id"),
            ("data/v2/test/dataset_test.jsonl", "id"),
            ("data/v1/test/dataset_test.jsonl", "id"))


def _md_escape(text: str) -> str:
    # 数学片段会由渲染器先保护；只转义公式外的Markdown表格竖线。
    # TeX中的 | 是绝对值，\| 是双竖线，不能互相替换。
    pieces = re.split(r"(\$\$.*?\$\$|\$[^$\n]+?\$)", text, flags=re.S)
    return "".join(piece if i % 2 else piece.replace("|", "\\|")
                   .replace("\r\n", "\n").replace("\n", " ")
                   for i, piece in enumerate(pieces))


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
    # 组合屏只在现有考点标签上作诊断。考点重复和泄漏候选不是同一
    # 标注任务,独立泄漏标签缺失时不得宣称已经校准。
    screen_t = Fraction(2, 5)
    for pair in labeled:
        pair["screen_prediction"] = (
            "重复" if pair["kp_j"] == "1" and Fraction(pair["jaccard"]) >= screen_t
            else "不重复")
    lk_tp = sum(p["label"] == "重复" and p["screen_prediction"] == "重复" for p in labeled)
    lk_fn = sum(p["label"] == "重复" and p["screen_prediction"] != "重复" for p in labeled)
    lk_fp = sum(p["label"] == "不重复" and p["screen_prediction"] == "重复" for p in labeled)
    lk_tn = sum(p["label"] == "不重复" and p["screen_prediction"] != "重复" for p in labeled)
    lk_pos, lk_neg = lk_tp + lk_fn, lk_fp + lk_tn
    recall = Fraction(lk_tp, lk_pos) if lk_pos else None
    fpr = Fraction(lk_fp, lk_neg) if lk_neg else None
    meets_targets = (recall is not None and fpr is not None
                     and recall >= MIN_RECALL and fpr <= MAX_FPR)
    excluded = [{"a": p["a"], "b": p["b"], "j5": p["jaccard"],
                 "reason": "当前组合屏未命中;保留原考点重复标签,仍计入 FN"}
                for p in labeled
                if p["label"] == "重复" and p["screen_prediction"] != "重复"]
    leakage_screen_calibration = {
        "rule": "考点签名一致 AND 5-gram Jaccard达阈值",
        "threshold": str(screen_t), "calibrated": False,
        "meets_original_pair_targets": meets_targets,
        "sample_scope": "原考点标签上的诊断;尚无独立泄漏标签",
        "tp": lk_tp, "fp": lk_fp, "fn": lk_fn, "tn": lk_tn,
        "precision": _ratio(lk_tp, lk_tp + lk_fp),
        "recall_all_labels": _ratio(lk_tp, lk_pos),
        "fpr": _ratio(lk_fp, lk_neg), "fnr": _ratio(lk_fn, lk_pos),
        "excluded_variants": excluded,
        "note": (f"当前 {len(labeled)} 对原考点标注上的召回率 "
                 f"{_ratio(lk_tp, lk_pos)},误报率 {_ratio(lk_fp, lk_neg)};"
                 f"{'达到' if meets_targets else '未达到'}原目标召回率≥19/20且误报率≤1/100。"
                 "组合屏的独立泄漏标注与匹配验收尚未完成,保持 UNCALIBRATED;"
                 "TP/(TP+FP) 是精确率,不得写成作用域召回率,不得按预测条件排除 FN。")}
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
            "leakage_screen_calibration": leakage_screen_calibration,
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
              "", "## 防泄漏屏诊断(尚未校准)", ""]
    lk = report.get("leakage_screen_calibration", {})
    if lk:
        lines += [f"- 执行规则:{lk.get('rule', '')};文字阈值 {lk.get('threshold', '')}。",
                  "- 状态:**UNCALIBRATED**,不能解除训练就绪门禁。",
                  f"- 原考点标注对照:TP {display(lk.get('tp'))},FP {display(lk.get('fp'))},"
                  f"FN {display(lk.get('fn'))},TN {display(lk.get('tn'))};"
                  f"精确率 {display(lk.get('precision'))},召回率 {display(lk.get('recall_all_labels'))},"
                  f"误报率 {display(lk.get('fpr'))},漏报率 {display(lk.get('fnr'))}。",
                  f"- {lk.get('note', '')}"]
        for ex in lk.get("excluded_variants", []):
            lines.append(f"- 未命中正例:{ex['a']} × {ex['b']}(J5={ex['j5']})——{ex['reason']}")
    lines += ["", "## 全对证据(48 对;J5 为文字 5-gram Jaccard,仅对照)", "",
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
    ap.add_argument("--out", type=Path, default=ROOT / "reviews/b5-candidates" / ("calibration-"+uuid.uuid4().hex))
    args = ap.parse_args(argv)
    raw = args.annotation.read_bytes()
    try:
        report = build_report(json.loads(raw))
    except (ValueError, KeyError, TypeError) as error:
        ap.error(str(error))
    report["annotation_sha256"] = hashlib.sha256(raw).hexdigest()
    try:
        args.out=new_output_dir(args.out)
    except (OSError,ValueError) as error:
        ap.error(str(error))
    report["qualification"]="DEVELOPMENT_DIAGNOSTIC_NOT_INDEPENDENT_CALIBRATION"
    with (args.out / "b5-calibration-report.json").open("x",encoding="utf-8") as output:
        output.write(json.dumps(report,ensure_ascii=False,indent=2))
    with (args.out / "b5-calibration-report.md").open("x",encoding="utf-8") as output:
        output.write(render_markdown(report))
    print(json.dumps({"calibrated": report["calibration"]["calibrated"],
                      "note": report["calibration"]["note"],
                      "mismatches": report["mismatches"]},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
