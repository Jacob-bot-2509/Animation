"""全部数据集的公式渲染风险静态扫描(只读)。"""
import json
import pathlib
import re
import collections

CJK = re.compile(r"[\u4e00-\u9fff]")
FW = re.compile(r"[\uff01-\uff5e\u3000-\u303f]")
MATH = re.compile(r"\$([^$]*)\$")
LEFT = re.compile(r"\\left\b")
RIGHT = re.compile(r"\\right\b")
RISK = [("裸 +infty", re.compile(r"\+infty")),
        ("裸 arctan/lim/sin 等(无反斜杠)", re.compile(r"(?<!\\)\b(?:arctan|arcsin|lim|sin|cos|tan|ln|log|exp|max|min|sup|inf|sum|int)\b")),
        ("未加花括号多位上下标", re.compile(r"[\^_]\d{2,}")),
        ("空公式 $ $", re.compile(r"^\s*$"))]

DATASETS = [
    ("v1 raw(63)", sorted(pathlib.Path("data/v1/raw").glob("*.jsonl"))),
    ("v2 train 池(现行)", sorted(pathlib.Path("data/v2/train/leakage-isolated-v3-2026-10-05").glob("*.jsonl"))),
    ("v2 eval", [pathlib.Path("data/v2/eval/dataset_eval.jsonl")]),
    ("v2 test", [pathlib.Path("data/v2/test/dataset_test.jsonl")]),
    ("drafts v4-final", sorted(pathlib.Path("reviews/2026-10-05-training-diversity-drafts").glob("batch-*/draft-codex-repair-v4-final.jsonl"))),
]

def text_fields(rec):
    out = []
    for k in ("problem", "solution", "answer"):
        if isinstance(rec.get(k), str):
            out.append((k, rec[k]))
    spec = rec.get("scene_spec")
    if isinstance(spec, dict):
        for k in ("objects", "steps"):
            for i, s in enumerate(spec.get(k) or []):
                if isinstance(s, str):
                    out.append((f"scene_spec.{k}[{i}]", s))
    return out

grand = collections.Counter()
print(f"{'数据集':22s} {'记录':>5s} {'公式':>6s} {'$奇偶异常':>9s} {'花括号不平衡':>11s} {'left/right':>10s} {'公式内CJK':>9s} {'公式内全角':>9s} {'风险':>5s}")
for name, paths in DATASETS:
    n_rec = n_math = n_odd = n_brace = n_lr = n_cjk = n_fw = n_risk = 0
    samples = collections.defaultdict(list)
    for p in paths:
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            n_rec += 1
            for fld, txt in text_fields(rec):
                if txt.count("$") % 2:
                    n_odd += 1
                    samples["$奇偶"].append((p.name, rec.get("id"), fld, txt[:70]))
                for m in MATH.finditer(txt):
                    span = m.group(1)
                    n_math += 1
                    if span.count("{") != span.count("}"):
                        n_brace += 1
                        samples["花括号"].append((p.name, rec.get("id"), fld, span[:70]))
                    if len(LEFT.findall(span)) != len(RIGHT.findall(span)):
                        n_lr += 1
                        samples["left/right"].append((p.name, rec.get("id"), fld, span[:70]))
                    if CJK.search(span):
                        n_cjk += 1
                        samples["公式内CJK"].append((p.name, rec.get("id"), fld, span[:70]))
                    if FW.search(span):
                        n_fw += 1
                        samples["公式内全角"].append((p.name, rec.get("id"), fld, span[:70]))
                    for label, pat in RISK:
                        if pat.search(span):
                            n_risk += 1
                            samples["风险:" + label].append((p.name, rec.get("id"), fld, span[:70]))
                            break
    print(f"{name:22s} {n_rec:>5d} {n_math:>6d} {n_odd:>9d} {n_brace:>11d} {n_lr:>10d} {n_cjk:>9d} {n_fw:>9d} {n_risk:>5d}")
    for k, v in samples.items():
        for s in v[:2]:
            print(f"      [{k}] {s[0]} {s[1]} {s[2]}: {s[3]}")
    for k, v in samples.items():
        grand[k] += len(v)
    grand["记录"] += n_rec
    grand["公式"] += n_math
print()
print("合计:", dict(grand))
