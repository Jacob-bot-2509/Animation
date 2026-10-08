"""eval/test 审阅稿 md → JSON 数组(待转换容器)。

契约:DATASET_SCHEMA.md + EVAL_TEST_PREP.md §3.5。
- eval:每道题每个解法一行,problem_id/solution_id/method 复合身份
  (GS3:同 problem_id 同题干、method 唯一);
- test:每题一行,id 全局唯一;
- scene_spec 由已复查的"动画要点"展开生成(objects=要点条目,
  steps=方法/知识点开场→要点逐步→结论),candidate 语义,后续可精修;
- source=self-authored(用户可改),license=Internal-Research-Use-Only;
- 涉及知识点/思路展开 不在正式字段契约内,仅保留于 md,不写入 JSON。

用法: python tools/make_eval_test.py
输出: data/v1/eval/dataset_eval.json、data/v1/test/dataset_test.json
(JSONL 由 tools/dataset_intake.py convert 生成,本脚本不直接写入口)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD_EVAL = ROOT / "dataset-eval.md"
MD_TEST = ROOT / "data-test.md"
OUT_EVAL = ROOT / "data" / "v1" / "eval"
OUT_TEST = ROOT / "data" / "v1" / "test"

CN = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
      "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
CN_REV = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]

FIELD_RE = re.compile(r"^\*\*(.+?)\*\*\s?(.*)$")
SOL_RE = re.compile(r"^解法([一二三四五六七八九十]+)（(.+)）$")


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
                   "fields": {}, "solutions": [], "anim": []}
            blocks.append(cur)
            continue
        if cur is None or not line.startswith("**"):
            continue
        m = FIELD_RE.match(line)
        if not m:
            continue
        label, content = m.group(1), m.group(2).strip()
        sol = SOL_RE.match(label)
        if sol:
            k = CN.get(sol.group(1))
            if k is None:
                print(f"[WARN] {cur['pid']}: 无法解析解法序号 {sol.group(1)}")
                continue
            cur["solutions"].append((k, sol.group(2).strip(), content))
        elif label == "题目":
            cur["fields"]["problem"] = content
        elif label == "答案":
            cur["fields"]["answer"] = content
        elif label == "解答":
            cur["fields"]["solution"] = content
        elif label == "动画要点":
            cur["anim"] = [p.strip() for p in content.split(" - ") if p.strip()]
        elif label == "涉及知识点":
            cur["fields"]["knowledge"] = content
    return blocks


def anim_points(block: dict) -> list[str]:
    pts = block["anim"]
    if not pts:
        print(f"[WARN] {block['pid']}: 缺动画要点")
    return pts


def eval_spec(block: dict, method: str) -> dict:
    pts = anim_points(block)
    objects = [f"{method}核心图形"] + list(pts)
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


def build_eval(blocks: list[dict]) -> list[dict]:
    records: list[dict] = []
    for b in blocks:
        sols = sorted(b["solutions"], key=lambda t: t[0])
        if len(sols) < 2:
            print(f"[WARN] {b['pid']}: 解法数 {len(sols)} < 2(同题多解要求)")
        for k, method, text in sols:
            records.append({
                "problem_id": b["pid"],
                "solution_id": f"{b['pid']}-s{k}",
                "method": method,
                "category": b["category"],
                "sub_category": b["sub_category"],
                "problem": b["fields"].get("problem", ""),
                "solution": text,
                "answer": b["fields"].get("answer", ""),
                "scene_spec": eval_spec(b, method),
                "source": "self-authored",
                "license": "Internal-Research-Use-Only",
            })
    return records


def build_test(blocks: list[dict]) -> list[dict]:
    records: list[dict] = []
    for b in blocks:
        records.append({
            "id": b["pid"],
            "category": b["category"],
            "sub_category": b["sub_category"],
            "problem": b["fields"].get("problem", ""),
            "solution": b["fields"].get("solution", ""),
            "answer": b["fields"].get("answer", ""),
            "scene_spec": test_spec(b),
            "source": "self-authored",
            "license": "Internal-Research-Use-Only",
        })
    return records


def main() -> int:
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
                        encoding="utf-8")
        print(f"{path} ← {len(recs)} 条")
    print("下一步: tools/dataset_intake.py convert <json> <jsonl> 生成正式入口")
    return 0


if __name__ == "__main__":
    sys.exit(main())
