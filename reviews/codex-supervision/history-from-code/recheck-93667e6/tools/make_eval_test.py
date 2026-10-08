"""eval/test 审阅稿 md → JSON 数组(待转换容器)。

契约:DATASET_SCHEMA.md + EVAL_TEST_PREP.md §3.5。
- eval:每道题每个解法一行,problem_id/solution_id/method 复合身份
  (GS3:同 problem_id 同题干、method 唯一);
- test:每题一行,id 全局唯一;
- scene_spec 由"动画要点"展开生成(objects=要点条目,
  steps=方法/知识点开场→要点逐步→结论);
  v2(2026-10-03 用户批准):eval 采用**逐解法动画要点**
  ("**解法k动画要点**"行),solution→scene_spec 一一对应;
  test 沿用问题级"**动画要点**"。
- source=self-authored(用户可改),license=Internal-Research-Use-Only;
- 涉及知识点/思路展开 不在正式字段契约内,仅保留于 md,不写入 JSON。

用法: python tools/make_eval_test.py [--out data/v2]
输出: <out>/eval/dataset_eval.json、<out>/test/dataset_test.json
(JSONL 由 tools/dataset_intake.py convert 生成,本脚本不直接写入口)
v1 目录与冻结数据只读,绝不覆盖。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD_EVAL = ROOT / "dataset-eval.md"
MD_TEST = ROOT / "data-test.md"
OUT_EVAL = ROOT / "data" / "v2" / "eval"   # v2 默认输出到 data/v2(独立目录)
OUT_TEST = ROOT / "data" / "v2" / "test"

sys.path.insert(0, str(ROOT / "tools"))
from meta_eval_test import META_EVAL, META_TEST  # noqa: E402

CN = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
      "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
CN_REV = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]

# 复查方 4 条逐解法 scene_spec 验收示例(msg_262,reviewer_example,逐字采纳):
# reviews/2026-10-03-claude-supervision/evidence/scene-spec-review-examples.json
REVIEWER_OVERRIDES: dict[str, dict] = {
    "eval-calc-023-s1": {
        "objects": ["坐标系与曲线 $f(x)=1/x^2$（$x\\ge1$）",
                    "积分区域 $1\\le x\\le R$ 及面积 $1-1/R$",
                    "正项级数 $\\sum_{n=1}^{\\infty}1/n^2$ 与积分判别法条件"],
        "steps": ["画出正值递减曲线 $f(x)=1/x^2$，明确连续、非负、递减三项条件。",
                  "用参数 $R>1$ 高亮曲线下从 $1$ 到 $R$ 的区域，展示 $\\int_1^R x^{-2}\\,dx=1-1/R$。",
                  "令 $R\\to\\infty$，面积趋于 $1$，说明反常积分收敛。",
                  "逐项对应 $a_n=f(n)$，应用积分判别法得到 $\\sum1/n^2$ 收敛"]},
    "eval-calc-023-s2": {
        "objects": ["项 $1/n^2$ 与比较项 $1/[n(n-1)]$（$n\\ge2$）",
                    "裂项恒等式 $1/[n(n-1)]=1/(n-1)-1/n$",
                    "部分和 $S_N$ 与上界 $2-1/N$"],
        "steps": ["从 $n\\ge2$ 开始，展示 $1/n^2<1/[n(n-1)]$；首项 $1$ 单独保留。",
                  "把比较项拆成 $1/(n-1)-1/n$，按相邻项逐项抵消。",
                  "给出 $S_N<1+\\sum_{n=2}^{N}(1/(n-1)-1/n)=2-1/N<2$（$N\\ge2$）。",
                  "展示 $S_N$ 递增且有上界，应用单调有界原则证明收敛"]},
    "eval-calc-023-s3": {
        "objects": ["数列 $a_n=1/n^2$ 及按 $2^k$ 标记的分块",
                    "凝聚项 $2^k a_{2^k}=2^{-k}$",
                    "几何级数 $\\sum_{k=1}^{\\infty}2^{-k}$"],
        "steps": ["确认 $a_n$ 正且递减，说明 Cauchy 凝聚判别法的适用条件。",
                  "高亮 $2^k$ 对应的样本位置和权重，建立 $2^k/(2^k)^2=2^{-k}$。",
                  "把凝聚级数映射到公比 $1/2$ 的几何级数，其和为 $1$；有限初始项不影响收敛性。",
                  "应用凝聚判别法回到原级数，结论是收敛"]},
    "eval-prob-010-s2": {
        "objects": ["固定点人数 $X$ 的分布柱状图 $P(X=k)=\\binom{n}{k}D(n-k)/n!$",
                    "错排数 $D(m)$ 与生成函数 $G(z)=\\sum_{k=0}^{n}P(X=k)z^k$",
                    "导数求和 $G^{\\prime}(1)=\\sum_{k=1}^{n}kP(X=k)$",
                    "按固定点个数分类的 $n-1$ 元素排列示意"],
        "steps": ["固定 $n$，按 $k$ 展示分布柱状图与组合表达式。",
                  "写出生成函数 $G(z)$ 并逐项求导得 $G^{\\prime}(1)$ 的求和式。",
                  "用 $k\\binom{n}{k}=n\\binom{n-1}{k-1}$ 把求和化为按固定点分类计数。",
                  "由 $\\sum_j\\binom{n-1}{j}D(n-1-j)=(n-1)!$ 得 $E[X]=1$"]},
}

FIELD_RE = re.compile(r"^\*\*(.+?)\*\*\s?(.*)$")
SOL_RE = re.compile(r"^解法([一二三四五六七八九十]+)（(.+)）$")
SOL_ANIM_RE = re.compile(r"^解法([一二三四五六七八九十]+)动画要点$")


def parse_blocks(md_path: Path, prefix: str) -> list[dict]:
    """按 '### <id> …' 切块并解析字段;返回 [{head, fields, solutions, anim}]。"""
    blocks: list[dict] = []
    cur: dict | None = None
    for raw in md_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("### "):
            rest = line[4:].strip()
            pid, _, catpart = rest.partition(" ")
            if not pid.startswith(prefix + "-"):
                cur = None
                continue
            category, _, sub = catpart.partition("·")
            cur = {"head": line, "pid": pid.strip(),
                   "category": category.strip(), "sub_category": sub.strip(),
                   "fields": {}, "solutions": [], "anim": [], "sol_anim": {}}
            blocks.append(cur)
            continue
        if cur is None or not line.startswith("**"):
            continue
        m = FIELD_RE.match(line)
        if not m:
            continue
        label, content = m.group(1), m.group(2).strip()
        sol = SOL_RE.match(label)
        sol_anim = SOL_ANIM_RE.match(label)
        if sol:
            k = CN.get(sol.group(1))
            if k is None:
                print(f"[WARN] {cur['pid']}: 无法解析解法序号 {sol.group(1)}")
                continue
            cur["solutions"].append((k, sol.group(2).strip(), content))
        elif sol_anim:
            k = CN.get(sol_anim.group(1))
            pts = [p.strip() for p in content.split(" - ") if p.strip()]
            pts = [p[2:].strip() if p.startswith("- ") else p for p in pts]
            if k is not None:
                cur["sol_anim"][k] = pts
        elif label == "题目":
            cur["fields"]["problem"] = content
        elif label == "答案":
            cur["fields"]["answer"] = content
        elif label == "解答":
            cur["fields"]["solution"] = content
        elif label == "动画要点":
            cur["anim"] = [p.strip() for p in content.split(" - ") if p.strip()]
            # F011:剔除残留的 Markdown 项目符号前缀(首个条目带 "- ")
            cur["anim"] = [p[2:].strip() if p.startswith("- ") else p
                           for p in cur["anim"]]
        elif label == "涉及知识点":
            cur["fields"]["knowledge"] = content
    return blocks


def anim_points(block: dict) -> list[str]:
    pts = block["anim"]
    if not pts:
        print(f"[WARN] {block['pid']}: 缺动画要点")
    return pts


def sol_anim_points(block: dict, k: int) -> list[str]:
    """v2:逐解法动画要点;缺失则该解法不生成(硬性自检,防回退 v1 共享场景)。"""
    pts = block.get("sol_anim", {}).get(k)
    if not pts:
        print(f"[FAIL] {block['pid']}-s{k}: 缺逐解法动画要点(v2 要求逐解法对应)")
        raise SystemExit(1)
    return pts


def eval_spec(block: dict, method: str, k: int) -> dict:
    rid = f"{block['pid']}-s{k}"
    if rid in REVIEWER_OVERRIDES:   # 复查方验收示例逐字采纳(msg_262)
        return REVIEWER_OVERRIDES[rid]
    pts = sol_anim_points(block, k)   # 逐解法要点(solution→scene_spec 对应)
    objects = list(pts)
    steps = [f"第一步：以{method}为主线，建立{block['category']}·"
             f"{block['sub_category']}场景并呈现该解法的关键图形。"]
    for i, pt in enumerate(pts):
        steps.append(f"第{CN_REV[i + 1]}步：{pt}。")
    steps.append(f"第{CN_REV[len(pts) + 1]}步：高亮最终结果与答案。")
    return {"objects": objects, "steps": steps}


def test_spec(block: dict) -> dict:
    pts = anim_points(block)
    know = block["fields"].get("knowledge", "")
    objects = list(pts)
    know_txt = f"呈现与{know}相关的核心图形" if know else "呈现核心图形"
    steps = [f"第一步：建立{block['category']}·{block['sub_category']}综合场景，"
             f"{know_txt}。"]
    for i, pt in enumerate(pts):
        steps.append(f"第{CN_REV[i + 1]}步：{pt}。")
    steps.append(f"第{CN_REV[len(pts) + 1]}步：高亮最终结果与答案。")
    return {"objects": objects, "steps": steps}


def _meta(pool: dict, pid: str) -> tuple[str, str]:
    if pid not in pool:
        print(f"[FAIL] {pid}: 缺元数据(META)")
        raise SystemExit(1)
    return pool[pid]


def build_eval(blocks: list[dict]) -> list[dict]:
    records: list[dict] = []
    for b in blocks:
        sols = sorted(b["solutions"], key=lambda t: t[0])
        if len(sols) < 2:
            print(f"[WARN] {b['pid']}: 解法数 {len(sols)} < 2(同题多解要求)")
        fam, style = _meta(META_EVAL, b["pid"])
        for k, method, text in sols:
            records.append({
                "id": f"{b['pid']}-s{k}",   # 全局唯一 id(下游按 §2 校验不受影响)
                "problem_id": b["pid"],
                "solution_id": f"{b['pid']}-s{k}",
                "method": method,
                "category": b["category"],
                "sub_category": b["sub_category"],
                "problem": b["fields"].get("problem", ""),
                "solution": text,
                "answer": b["fields"].get("answer", ""),
                "scene_spec": eval_spec(b, method, k),
                "function_family": fam,
                "visual_style": style,
                "efficiency_tags": sol_anim_points(b, k),
                "source": "self-authored",
                "license": "Internal-Research-Use-Only",
            })
    return records


def build_test(blocks: list[dict]) -> list[dict]:
    records: list[dict] = []
    for b in blocks:
        fam, style = _meta(META_TEST, b["pid"])
        records.append({
            "id": b["pid"],
            "category": b["category"],
            "sub_category": b["sub_category"],
            "problem": b["fields"].get("problem", ""),
            "solution": b["fields"].get("solution", ""),
            "answer": b["fields"].get("answer", ""),
            "scene_spec": test_spec(b),
            "function_family": fam,
            "visual_style": style,
            "efficiency_tags": anim_points(b),
            "source": "self-authored",
            "license": "Internal-Research-Use-Only",
        })
    return records


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "data" / "v2"),
                    help="输出根目录(默认 data/v2;绝不写 data/v1)")
    args = ap.parse_args()
    global OUT_EVAL, OUT_TEST
    OUT_EVAL = Path(args.out) / "eval"
    OUT_TEST = Path(args.out) / "test"
    # msg_264:大小写不敏感 + 解析路径后再判断,防 Windows --out data/V1 绕过
    out_resolved = Path(args.out).resolve()
    if any(p.lower() == "v1" for p in out_resolved.parts):
        print("[FAIL] 拒绝写入 data/v1 任何大小写形式(v1 冻结数据只读)")
        return 1
    eval_blocks = parse_blocks(MD_EVAL, "eval")
    test_blocks = parse_blocks(MD_TEST, "test")
    eval_recs = build_eval(eval_blocks)
    test_recs = build_test(test_blocks)
    if len(eval_blocks) != 100:
        print(f"[WARN] eval 题数 {len(eval_blocks)} != 100")
    if len(test_blocks) != 150:
        print(f"[WARN] test 题数 {len(test_blocks)} != 150")
    # 同 problem_id 同题干 + method 唯一(GS3)自检
    by_pid: dict[str, list[dict]] = {}
    for r in eval_recs:
        by_pid.setdefault(r["problem_id"], []).append(r)
    for pid, items in by_pid.items():
        texts = {r["problem"] for r in items}
        methods = [r["method"] for r in items]
        if len(texts) != 1:
            print(f"[FAIL] {pid}: 同 problem_id 题干不一致")
            return 1
        if len(methods) != len(set(methods)):
            print(f"[FAIL] {pid}: method 重复")
            return 1
    OUT_EVAL.mkdir(parents=True, exist_ok=True)
    OUT_TEST.mkdir(parents=True, exist_ok=True)
    for path, recs in [(OUT_EVAL / "dataset_eval.json", eval_recs),
                       (OUT_TEST / "dataset_test.json", test_recs)]:
        path.write_text(json.dumps(recs, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8", newline="\n")  # LF 落盘
        print(f"{path} ← {len(recs)} 条")
    print("下一步: tools/dataset_intake.py convert <json> <jsonl> 生成正式入口")
    return 0


if __name__ == "__main__":
    sys.exit(main())
