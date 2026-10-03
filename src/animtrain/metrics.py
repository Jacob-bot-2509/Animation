"""固定评测指标契约(B3,纯标准库):第一轮训练任务的指标定义、
逐样本结果 schema 与失败分类。所有组比较/逐样本评测必须共用此契约,
分母不得因失败缩小;未测项标 NOT_MEASURED,不假绿。
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

# 失败分类(固定口径,逐样本必须落一类)
FAILURE_TAXONOMY = (
    "api_error",          # 模型 API 幻觉/非法调用
    "latex_error",        # LaTeX 语法/渲染问题
    "schema_violation",   # JSON/字段结构不合规
    "truncated",          # 输出截断(未闭合/超长)
    "math_error",         # 数学语义错误(须经规则/人工复核)
    "render_fail",        # 渲染失败(有 code 时才适用)
    "other",              # 其余(必须附原因)
)

# 第一轮任务(problem+solution → scene_spec)的固定指标名
FIXED_METRICS = (
    "strict_parse_rate",          # 严格 JSON 整体可解析率
    "lenient_parse_rate",         # 宽松提取率
    "spec_field_compliance_rate", # objects/steps 字段合规率
    "math_review_pass_rate",      # 人工复核通过率(未标注 → NOT_MEASURED)
    "median_latency_sec",         # 中位延迟
    "p95_latency_sec",
)


@dataclass
class SampleResult:
    """逐样本结果(固定 schema;训练/评测输出共用)。"""
    sample_id: str
    input_hash: str                 # 输入(problem+solution)哈希
    output_hash: str = ""           # 原始输出哈希
    parsed_strict: bool = False
    parsed_lenient: bool = False
    spec_problems: list[str] = field(default_factory=list)
    failure_class: str = ""         # 失败时必填(FAILURE_TAXONOMY 之一)
    failure_detail: str = ""
    metrics: dict = field(default_factory=dict)  # 指标值(可含 latency 等)
    status: str = "pending"         # pending|ok|failed

    def to_dict(self) -> dict:
        return {"sample_id": self.sample_id, "input_hash": self.input_hash,
                "output_hash": self.output_hash,
                "parsed_strict": self.parsed_strict,
                "parsed_lenient": self.parsed_lenient,
                "spec_problems": self.spec_problems,
                "failure_class": self.failure_class,
                "failure_detail": self.failure_detail,
                "metrics": self.metrics, "status": self.status}


def finalize_result(r: SampleResult) -> SampleResult:
    """按解析与失败状态定稿:失败必须落分类;分母固定为样本总数。"""
    if r.parsed_lenient and not r.spec_problems:
        r.status = "ok"
    else:
        r.status = "failed"
        if not r.failure_class:
            r.failure_class = "schema_violation" if r.parsed_lenient else "other"
        if r.failure_class not in FAILURE_TAXONOMY:
            raise ValueError(f"failure_class 非法: {r.failure_class!r}")
        if not r.failure_detail:
            r.failure_detail = "未提供失败原因(契约要求必须附原因)"
    return r


def aggregate(results: list[SampleResult], math_review: dict | None = None) -> dict:
    """固定口径汇总:分母 = 样本总数,失败不缩小分母;未标注项 NOT_MEASURED。"""
    n = len(results)
    if n == 0:
        return {"n_samples": 0, "error": "空结果集不可汇总"}
    ok = sum(1 for r in results if r.status == "ok")
    strict = sum(1 for r in results if r.parsed_strict)
    lenient = sum(1 for r in results if r.parsed_lenient)
    lat = sorted(r.metrics.get("latency_sec", 0.0) for r in results
                 if r.metrics.get("latency_sec") is not None)
    failure_counts: dict[str, int] = {}
    for r in results:
        if r.status == "failed":
            failure_counts[r.failure_class] = failure_counts.get(r.failure_class, 0) + 1
    mr = "NOT_MEASURED"
    mr_n = 0
    if math_review and n:
        mr_n = sum(1 for v in math_review.values() if v is True)
        mr = round(mr_n / n, 4)
    if lat:
        mid = len(lat) // 2
        median = (lat[mid - 1] + lat[mid]) / 2 if len(lat) % 2 == 0 else lat[mid]
        p95 = lat[min(len(lat) - 1, int(len(lat) * 0.95))]
    else:
        median, p95 = None, None
    return {"n_samples": n, "ok": ok, "ok_rate": round(ok / n, 4),
            "strict_parse_rate": round(strict / n, 4),
            "lenient_parse_rate": round(lenient / n, 4),
            "spec_field_compliance_rate": round(ok / n, 4),  # ok=字段合规(当前口径)
            "math_review_pass_rate": mr,
            "math_review_n": mr_n,
            "median_latency_sec": median,
            "p95_latency_sec": p95,
            "failure_counts": failure_counts}


def sample_hash(problem: str, solution: str) -> str:
    return hashlib.sha256(
        json.dumps({"problem": problem, "solution": solution},
                   ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()
