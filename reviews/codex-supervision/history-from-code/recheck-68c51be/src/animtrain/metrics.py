"""固定评测指标契约(B3,纯标准库):第一轮训练任务的指标定义、
逐样本结果 schema 与失败分类。所有组比较/逐样本评测必须共用此契约,
分母不得因失败缩小;未测项标 NOT_MEASURED,不假绿。
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, field, replace

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


METRIC_CONTRACT_VERSION = 1


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
    """Preserve explicit failures even when the JSON and its fields are valid."""
    if r.status not in ("pending", "ok", "failed"):
        raise ValueError(f"status invalid: {r.status!r}")
    if r.failure_class and r.failure_class not in FAILURE_TAXONOMY:
        raise ValueError(f"failure_class invalid: {r.failure_class!r}")
    for flag in ("parsed_strict", "parsed_lenient"):
        if type(getattr(r, flag)) is not bool:
            raise ValueError(f"{flag} must be bool, got {getattr(r, flag)!r}")
    if r.parsed_strict and not r.parsed_lenient:
        raise ValueError("Strict parsing success requires lenient parsing success")
    field_ok = r.parsed_lenient and not r.spec_problems
    if field_ok and not r.failure_class and r.status != "failed":
        r.status = "ok"
    else:
        r.status = "failed"
        if not r.failure_class:
            r.failure_class = "schema_violation" if r.parsed_lenient else "other"
        if not r.failure_detail:
            r.failure_detail = "Failure reason was not provided"
    return r


def aggregate(results: list[SampleResult], math_review: dict | None = None) -> dict:
    """All rates use the full sample count. Partial math review remains unmeasured.

    Field compliance is independent of semantic/runtime success. Latencies use
    measured samples only, with nearest-rank p95; latency_n records coverage.
    Copies are finalized so aggregation never rewrites the caller's records.
    """
    n = len(results)
    if n == 0:
        return {"n_samples": 0, "error": "Empty result set cannot be aggregated"}
    sample_ids = [r.sample_id for r in results]
    if len(set(sample_ids)) != n:
        raise ValueError("Duplicate sample_id in result set")
    review = math_review if math_review is not None else {}
    if not isinstance(review, dict):
        raise ValueError("math_review must be a sample_id mapping")
    foreign = set(review) - set(sample_ids)
    if foreign:
        raise ValueError("math_review contains sample IDs outside this result set")
    if any(v is not None and type(v) is not bool for v in review.values()):
        raise ValueError("math_review values must be bool or None")

    normalized = [finalize_result(replace(r)) for r in results]
    ok = sum(r.status == "ok" for r in normalized)
    strict = sum(r.parsed_strict for r in normalized)
    lenient = sum(r.parsed_lenient for r in normalized)
    field_ok = sum(r.parsed_lenient and not r.spec_problems for r in normalized)
    lat = []
    for r in normalized:
        value = r.metrics.get("latency_sec")
        if value is None:
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)) \
                or not math.isfinite(value) or value < 0:
            raise ValueError(f"Invalid latency_sec for {r.sample_id!r}")
        lat.append(value)
    lat.sort()
    failure_counts: dict[str, int] = {}
    for r in normalized:
        if r.status == "failed":
            failure_counts[r.failure_class] = failure_counts.get(r.failure_class, 0) + 1

    mr_n = sum(review.get(sid) is True for sid in sample_ids)
    reviewed_n = sum(type(review.get(sid)) is bool for sid in sample_ids)
    mr = round(mr_n / n, 4) if reviewed_n == n else "NOT_MEASURED"
    if lat:
        mid = len(lat) // 2
        median = (lat[mid - 1] + lat[mid]) / 2 if len(lat) % 2 == 0 else lat[mid]
        p95 = lat[math.ceil(len(lat) * 0.95) - 1]
    else:
        median, p95 = None, None
    return {"metric_contract_version": METRIC_CONTRACT_VERSION,
            "n_samples": n, "ok": ok, "ok_rate": round(ok / n, 4),
            "strict_parse_rate": round(strict / n, 4),
            "lenient_parse_rate": round(lenient / n, 4),
            "spec_field_compliance_rate": round(field_ok / n, 4),
            "math_review_pass_rate": mr,
            "math_review_n": mr_n, "math_reviewed_n": reviewed_n,
            "median_latency_sec": median, "p95_latency_sec": p95,
            "latency_n": len(lat), "failure_counts": failure_counts}


def sample_hash(problem: str, solution: str) -> str:
    return hashlib.sha256(
        json.dumps({"problem": problem, "solution": solution},
                   ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()
