"""把全部数据集的全部字段打成渲染包 MD(只读源数据,只写渲染包)。"""
import json
import pathlib

OUT = pathlib.Path("dataset_audit_2026-10-05-render-check/render-packs")
OUT.mkdir(parents=True, exist_ok=True)

DATASETS = [
    ("train-v1-raw-63", sorted(pathlib.Path("data/v1/raw").glob("*.jsonl"))),
    ("train-v2-pool-47", sorted(pathlib.Path("data/v2/train/leakage-isolated-v3-2026-10-05").glob("*.jsonl"))),
    ("eval-300", [pathlib.Path("data/v2/eval/dataset_eval.jsonl")]),
    ("test-150", [pathlib.Path("data/v2/test/dataset_test.jsonl")]),
    ("drafts-264-v4final", sorted(pathlib.Path("reviews/2026-10-05-training-diversity-drafts").glob("batch-*/draft-codex-repair-v4-final.jsonl"))),
]

summary = {}
for name, paths in DATASETS:
    parts = [f"# 渲染包 {name}\n"]
    n = 0
    for p in paths:
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            rid = rec.get("id") or rec.get("problem_id")
            n += 1
            parts.append(f"\n### {rid}\n")
            for k in ("problem", "solution", "answer"):
                v = rec.get(k)
                if isinstance(v, str) and v:
                    parts.append(f"**{k}** {v}\n")
            spec = rec.get("scene_spec")
            if isinstance(spec, dict):
                for i, s in enumerate(spec.get("objects") or []):
                    parts.append(f"**objects[{i}]** {s}\n")
                for i, s in enumerate(spec.get("steps") or []):
                    parts.append(f"**steps[{i}]** {s}\n")
    out = OUT / f"{name}.md"
    out.write_text("\n".join(parts), encoding="utf-8", newline="\n")
    n_formula = sum(1 for p in paths for line in p.read_text(encoding="utf-8").splitlines()
                    if line.strip() and "$" in line)
    summary[name] = {"records": n, "md_bytes": out.stat().st_size}
    print(f"{name:22s} 记录={n:>4d} md={out.stat().st_size:>9d} B -> {out}")
print()
print(json.dumps(summary, ensure_ascii=False, indent=1))
