# -*- coding: utf-8 -*-
"""核心范围一致性复验:对现役 761 条(47训练+264草稿+450评测/测试)逐条检查:
  ①三字段非空 ②LaTeX定界符/花括号平衡 ③答案与解析末式一致性(归一化字符串+sympy)
  ④小数作答(用户策略:有理数用分数)记WARN。只报告不修改。
输出 reviews/2026-10-07-gap-materials/core-submission-v1/consistency-report.jsonl。"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reviews/2026-10-07-gap-materials/core-submission-v1/consistency-report.jsonl"
if OUT.exists():
    raise ValueError("preserve previous report")

try:
    import sympy
    SYMPY_OK = True
except ImportError:
    SYMPY_OK = False


def norm(expr: str) -> str:
    t = expr.replace(" ", "").replace("　", "")
    t = t.replace("\\left", "").replace("\\right", "")
    t = t.replace("\\displaystyle", "").replace("\\quad", "")
    t = t.replace("{", "").replace("}", "")
    t = t.replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac")
    return t.strip().rstrip(".。;；")


def last_math_parts(sol: str):
    lines = [l.strip() for l in sol.splitlines() if l.strip()]
    if not lines:
        return "", ""
    segs = re.findall(r"\$([^$]+)\$", lines[-1])
    if not segs:
        return "", ""
    tail = segs[-1]
    eq = [i for i, ch in enumerate(tail) if ch == "="]
    rhs = tail[eq[-1] + 1:] if eq else tail
    return tail, rhs


def is_text_answer(ans: str) -> bool:
    return (not re.search(r"[\\^=]", ans)) and bool(re.search(r"[一-鿿]", ans))


def latex_balanced(text: str) -> bool:
    if text.count("$") % 2 != 0:
        return False
    depth = 0
    for ch in text:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def main() -> int:
    rows = []
    counts = {"total": 0, "pass": 0, "warn": 0, "fail": 0}

    def check(rid, rec, source):
        counts["total"] += 1
        problem, sol, ans = (rec.get("problem") or ""), (rec.get("solution") or ""), (rec.get("answer") or "")
        issues = []
        if not problem.strip() or not sol.strip() or not ans.strip():
            issues.append("empty_field")
        if not latex_balanced(problem + sol + ans):
            issues.append("latex_unbalanced")
        tail, rhs = last_math_parts(sol)
        if tail and ans:
            ans_norm = norm(ans.strip("$"))
            if ans_norm:
                if is_text_answer(ans_norm):
                    if ans_norm not in norm(sol[-80:]):
                        issues.append("tail_mismatch")
                elif norm(tail) != ans_norm and norm(rhs) != ans_norm:
                    issues.append("tail_mismatch")
                elif SYMPY_OK:
                    try:
                        a = sympy.sympify(ans_norm.replace("\\frac", "Rational"))
                        l = sympy.sympify(norm(rhs).replace("\\frac", "Rational"))
                        if sympy.simplify(a - l) != 0:
                            issues.append("sympy_value_mismatch")
                    except Exception:
                        pass  # 非纯数值/无法解析,跳过sympy
        if re.search(r"(?<!\d)\d+\.\d+(?!\d)", ans):
            issues.append("decimal_in_answer")
        status = "FAIL" if issues else "PASS"
        if status == "FAIL":
            counts["fail"] += 1
        else:
            counts["pass"] += 1
        rows.append({"id": rid, "source": source, "status": status,
                     "issues": issues,
                     "record_sha256": hashlib.sha256(
                         json.dumps(rec, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()})

    # 47 训练
    for f in sorted((ROOT / "data/v2/train/leakage-isolated-v3-2026-10-05").glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                check(json.loads(line)["id"], json.loads(line), f.name)
    # 450 评测/测试
    for f in [ROOT / "data/v2/eval/dataset_eval.jsonl", ROOT / "data/v2/test/dataset_test.jsonl"]:
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                check(rec["id"], rec, f.name)
    # 264 草稿(经选择器,raw_sha256 对原始字节)
    sel = json.loads((ROOT / "reviews/2026-10-05-training-diversity-drafts/draft-selection.json").read_text(encoding="utf-8"))
    for e in sel["entries"]:
        p = ROOT / "reviews/2026-10-05-training-diversity-drafts" / e["path"]
        raw = p.read_bytes()
        if hashlib.sha256(raw).hexdigest() != e["raw_sha256"]:
            raise ValueError("selector raw sha mismatch: " + e["path"])
        for line in raw.decode("utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                check(rec["id"], rec, e["batch"])

    with OUT.open("w", encoding="utf-8", newline="\n") as out:
        for r in rows:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("sympy available:", SYMPY_OK)
    print("counts:", counts)
    fails = [r for r in rows if r["status"] == "FAIL"]
    print("fail examples:", len(fails))
    for r in fails[:15]:
        print(" -", r["id"], r["issues"], "|", r["source"])
    print("report:", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
