"""近重复检测:5-gram shingle + Jaccard(前项目实测标准,独立重写,纯标准库)。

前项目经验(README 教训 2):仅精确重叠不够——改措辞/换数字的同一题
必须被近重复门禁拦住;且检测器必须先过对照(对已知近重复对报警、
对无关对静默),误报比漏报危险。

用法:
  from animtrain.near_dup import ShingleIndex
  idx = ShingleIndex()
  idx.add("题目 A 文本", meta={"id": "a"})
  sim, hit = idx.max_sim("题目 B 文本")   # sim ∈ [0,1],hit 为 meta
"""
from __future__ import annotations

import re
from collections import Counter

K = 5           # shingle 长度
THRESHOLD = 0.7  # 前项目标准:Jaccard ≥ 0.7 视为近重复


def norm_text(t: str) -> str:
    """归一化:去空白与常见符号,防用空格/换行绕检测。"""
    return re.sub(r"[\s$\\_{}\[\]()]", "", (t or "")).lower()


def shingles(text: str, k: int = K) -> set[str]:
    t = norm_text(text)
    if len(t) < k:
        return {t} if t else set()
    return {t[i:i + k] for i in range(len(t) - k + 1)}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    return inter / (len(a) + len(b) - inter)


class ShingleIndex:
    """倒排索引:shingle → 条目。用于在池子里快速找近重复候选。"""

    def __init__(self) -> None:
        self.index: dict[str, list[int]] = {}
        self.sets: list[set[str]] = []
        self.meta: list[dict] = []

    def add(self, text: str, meta: dict) -> None:
        s = shingles(text)
        i = len(self.sets)
        self.sets.append(s)
        self.meta.append(meta)
        for g in s:
            self.index.setdefault(g, []).append(i)

    def max_sim(self, text: str) -> tuple[float, dict | None]:
        s = shingles(text)
        if not s:
            return 0.0, None
        hits: Counter[int] = Counter()
        for g in s:
            for i in self.index.get(g, ()):
                hits[i] += 1
        best, best_i = 0.0, None
        for i, _ in hits.most_common(20):
            v = jaccard(s, self.sets[i])
            if v > best:
                best, best_i = v, i
        return best, (self.meta[best_i] if best_i is not None else None)


def find_near_dups(pool_texts: list[tuple[str, dict]], queries: list[tuple[str, dict]],
                   threshold: float = THRESHOLD) -> list[dict]:
    """把 pool 建索引,对 queries 逐个查近重复;返回超阈值的命中列表。"""
    idx = ShingleIndex()
    for text, meta in pool_texts:
        idx.add(text, meta)
    out = []
    for text, meta in queries:
        sim, hit = idx.max_sim(text)
        if sim >= threshold:
            out.append({"query": meta, "sim": round(sim, 3), "hit": hit})
    return out
