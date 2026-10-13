"""本质考点规则(模块+题型):B5 校准 v3 的判定核心,供数据门禁与去重管线复用。

规则(2026-10-04 用户裁决,48 对真实标注 + 8 处裁决,CALIBRATED 阈值 1):
- 本质考点 = (category, 题型);两道题考点签名一致 = 重复。
- 题型由题文动词分类,sub_category 兜底;缺 category/problem 或无法归类
  且无 sub → 拒绝签名(不得把缺失值当成共同考点)。
- 生产语义(用户裁决):同考点题**保留为变体**;防泄漏屏 = 签名一致
  AND 5-gram 文字相似 ≥ 阈值(见 animtrain.validate)。
"""
from __future__ import annotations


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
        raise ValueError("题型无法识别且缺少 sub_category,不能把缺失值当成共同考点")
    return f"其他[{sub}]"


def kp_signature(rec: dict) -> tuple[str, str]:
    if not isinstance(rec, dict):
        raise ValueError("结构化题目记录非对象(null/坏行),不能提取考点签名")
    if not isinstance(rec.get("category"), str) or not rec["category"].strip():
        raise ValueError("结构化题目缺少模块 category")
    if not isinstance(rec.get("problem"), str) or not rec["problem"].strip():
        raise ValueError("结构化题目缺少完整题文 problem")
    return (rec["category"], classify_kp(rec))


def kp_tokens(rec: dict) -> set[tuple[str, str]]:
    """字段带名的考点 token,模块与题型不得互相混淆。"""
    category, kind = kp_signature(rec)
    return {("category", category), ("kind", kind)}


def kp_jaccard(a: set[tuple[str, str]], b: set[tuple[str, str]]):
    from fractions import Fraction
    union = a | b
    return Fraction(len(a & b), len(union)) if union else Fraction(0)
