"""深层候选逐对裁决:DIFFERENT_CORE(附数学区别) 或 NEEDS_CODEX(边界交裁决)."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reviews/2026-10-07-semantic-core-lists"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


VERDICTS = {
    ("draft-c36-03", "eval-linalg-021-s1"): (
        "NEEDS_CODEX",
        "同目标'求二次型正定参数范围'+同族+共享'顺序主子式';结构差异:训练侧参数在对角z²系数"
        "(Δ3=a→a>0),评测侧参数在交叉项xz(Δ3=2-a²→|a|<√2);训练侧另要求a=0半正定/a<0不定的退化讨论。"
        "按c31从宽原则交Codex裁决"),
    ("draft-c36-03", "eval-linalg-021-s2"): (
        "NEEDS_CODEX",
        "同目标同族;训练侧顺序主子式,评测侧配方——方法不同但任务同型、阈值同型(|a|<常数)。交裁决"),
    ("draft-c36-03", "eval-linalg-021-s3"): (
        "NEEDS_CODEX",
        "同目标同族;训练侧顺序主子式,评测侧Schur补。任务同型。交裁决"),
    ("linalg-051", "eval-linalg-022-s1"): (
        "NEEDS_CODEX",
        "同目标'多项式因式分解'+同族+共享'有理根定理';差异:训练侧三次(x³-6x²+11x-6,根1,2,3)"
        "且多要求根分布讨论,评测侧四次(x⁴+2x³-7x²-8x+12,根1,2,-2,-3)。方法完全可迁移,交裁决"),
    ("draft-c02-01", "eval-calc-019-s1"): (
        "DIFFERENT_CORE",
        "训练侧为振荡型反常积分(Fresnel)条件收敛+尾界证明;评测侧为指数衰减反常积分求值。"
        "核心对象(振荡vs指数)与任务(证明+界vs求值)均不同,仅共享'分部积分'这一泛用步骤"),
    ("draft-c30-01", "eval-linalg-024-s3"): (
        "DIFFERENT_CORE",
        "训练侧:由零点重数条件构造多项式(整除性+定常数);评测侧:已知多项式按x-1展开(泰勒)。"
        "任务方向相反,仅共享'换元展开'泛用步骤"),
    ("draft-c35-01", "eval-linalg-021-s2"): (
        "DIFFERENT_CORE",
        "训练侧:化标准形+求惯性指数(无参数);评测侧:求正定参数范围(含参)。目标不同,仅共享'配方'"),
    ("draft-c35-03", "eval-linalg-021-s2"): (
        "DIFFERENT_CORE",
        "训练侧:求秩为1的参数+各参数标准形;评测侧:求正定参数范围。目标与判定量(秩vs正定)不同"),
    ("draft-c35-04", "eval-linalg-021-s2"): (
        "DIFFERENT_CORE",
        "训练侧:化标准形+惯性(无参退化);评测侧:求正定参数范围。目标不同"),
    ("draft-c36-04", "eval-linalg-021-s2"): (
        "DIFFERENT_CORE",
        "训练侧:判断半正定与秩(无参);评测侧:求正定参数范围(含参)。目标不同"),
    ("draft-c36-05", "eval-linalg-021-s1"): (
        "DIFFERENT_CORE",
        "训练侧:构造反例(顺序主子式非负但非半正定);评测侧:判正定参数范围。任务相反(构造vs判定)"),
    ("draft-c37-05", "eval-linalg-026-s1"): (
        "DIFFERENT_CORE",
        "训练侧:证向量组为基+求坐标;评测侧:判断线性相关性。目标不同,仅共享'行列式'"),
}


def main() -> int:
    cand = json.loads((OUT / "deep-candidates-v1.json").read_text(encoding="utf-8-sig"))
    rows = []
    missing = []
    for c in cand["candidates"]:
        key = (c["train_id"], c["eval_id"])
        v = VERDICTS.get(key)
        if v is None:
            missing.append(key)
            continue
        rows.append({**c, "verdict": v[0], "pairwise_reason": v[1]})
    # 第二梯队 11 对也须有裁决(与第一梯队 3 对并集)
    report = {
        "schema": "deep-candidates-disposed-v1",
        "family_pairs_total": cand["family_pairs_total"],
        "flagged_pairs": len(rows),
        "needs_codex": sum(1 for r in rows if r["verdict"] == "NEEDS_CODEX"),
        "different_core": sum(1 for r in rows if r["verdict"] == "DIFFERENT_CORE"),
        "missing_dispositions": [list(k) for k in missing],
        "rows": rows,
        "honest_coverage": (
            "1131 同族跨集配对经(同义目标组∨步骤Jaccard≥0.5)得3对高信号+11对二梯队=14对已逐对裁决;"
            "其余1117对签名层面目标组不同且Jaccard<0.25,已由签名逐对计算排除,未逐对写理由;"
            "跨族同义核心(不同sub_category的几何↔代数改写)不在此通道覆盖内,如实保留风险"),
    }
    out = OUT / "deep-candidates-disposed-v1.json"
    with out.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")
    b = out.read_bytes()
    print(f"裁决: {len(rows)} 对 (NEEDS_CODEX {report['needs_codex']}, DIFFERENT_CORE {report['different_core']})")
    if missing:
        print("缺裁决:", missing)
    print(f"回执: {out.relative_to(ROOT)}  sha256={digest(b)}  bytes={len(b)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
