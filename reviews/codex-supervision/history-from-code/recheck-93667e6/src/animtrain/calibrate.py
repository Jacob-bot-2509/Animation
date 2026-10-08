"""近重复阈值校准方法框架(B5,纯标准库)。

原理:构造**已标注**的对照集(已知近重复对 + 已知无关对),在阈值网格上
测 precision/recall/FPR/FNR,选满足质量目标的阈值并输出校准报告。
在真实数据校准完成前,阈值一律标 UNCALIBRATED,不得当已验收。

用法:
  from animtrain.calibrate import calibrate_threshold
  report = calibrate_threshold(pos_pairs, neg_pairs, idx_builder)
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .near_dup import ShingleIndex, jaccard


@dataclass
class CalibrationReport:
    threshold: float
    tp: int = 0
    fp: int = 0
    fn: int = 0
    tn: int = 0
    precision: float = 0.0
    recall: float = 0.0
    fpr: float = 0.0
    fnr: float = 0.0
    calibrated: bool = False
    note: str = ""
    grid: list[dict] = field(default_factory=list)


def evaluate_at(pool_texts: list[str], pos_queries: list[str],
                neg_queries: list[str], threshold: float) -> dict:
    """在给定阈值下,用已标注对照集测四项指标。"""
    idx = ShingleIndex()
    for t in pool_texts:
        idx.add(t, {"pool": True})
    tp = fp = 0
    for q in pos_queries:
        sim, _ = idx.max_sim(q)
        if sim >= threshold:
            tp += 1
        else:
            fp = 0  # 占位,下面统一算
    # 重算更清晰:pos 里 <阈值 = FN;neg 里 ≥阈值 = FP
    fn = sum(1 for q in pos_queries if idx.max_sim(q)[0] < threshold)
    tp = len(pos_queries) - fn
    fp = sum(1 for q in neg_queries if idx.max_sim(q)[0] >= threshold)
    tn = len(neg_queries) - fp
    def ratio(a, b):
        return round(a / b, 4) if b else None
    return {"threshold": threshold, "tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision": ratio(tp, tp + fp), "recall": ratio(tp, tp + fn),
            "fpr": ratio(fp, fp + tn), "fnr": ratio(fn, fn + tp)}


def calibrate_threshold(pool_texts: list[str], pos_queries: list[str],
                        neg_queries: list[str],
                        min_recall: float = 0.95,
                        max_fpr: float = 0.01,
                        grid_start: float = 0.3,
                        grid_end: float = 0.95,
                        grid_step: float = 0.05) -> CalibrationReport:
    """阈值网格扫描,选满足 min_recall 与 max_fpr 的最低阈值。

    报告 calibrated 状态:只有对照集标注可信且指标达标才 True;
    任何一项不达标 → calibrated=False + 说明(不伪造)。
    """
    best: dict | None = None
    grid: list[dict] = []
    t = grid_start
    while t <= grid_end + 1e-9:
        r = evaluate_at(pool_texts, pos_queries, neg_queries, t)
        grid.append(r)
        if (r["recall"] is not None and r["fpr"] is not None
                and r["recall"] >= min_recall and r["fpr"] <= max_fpr):
            best = r
            break
        t = round(t + grid_step, 6)
    if best is None:
        return CalibrationReport(
            threshold=0.0, calibrated=False, grid=grid,
            note=f"网格内无阈值同时满足 recall≥{min_recall} 且 fpr≤{max_fpr}"
                 "—— 对照集或方法需检查,当前阈值仍 UNCALIBRATED")
    return CalibrationReport(
        threshold=best["threshold"], tp=best["tp"], fp=best["fp"],
        fn=best["fn"], tn=best["tn"], precision=best["precision"],
        recall=best["recall"], fpr=best["fpr"], fnr=best["fnr"],
        calibrated=True, grid=grid,
        note=f"网格扫描选定 {best['threshold']}(recall={best['recall']},"
             f"fpr={best['fpr']});用于正式数据前须以真实分布对照集复跑")
