"""新版渲染包生成:candidate-sources(497条含40修订)为源,只读冻结交付,写新渲染包目录."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import argparse
import witness_transfer_common as _transfer

def _fresh_output(args):
    if args.out is None:
        raise ValueError("--execute requires --out with a new project directory")
    target = _transfer.path(args.out, root=ROOT, write=True)
    if target.exists():
        raise ValueError("Preserve previous output: " + str(target))
    target.mkdir(parents=True, exist_ok=False)
    return target

SUP = ROOT / "archives/reviews/codex-supervision/2026-10-07-math-batch-supervision"
OUT = ROOT / "archives/dataset-audits/dataset_audit_2026-10-07-render-check-v2"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def latex_balanced(text: str) -> bool:
    """轻量LaTeX定界符/花括号平衡(渲染前体检,不替代渲染)."""
    depth = 0
    in_math = False
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "$":
            if i + 1 < len(text) and text[i + 1] == "$":
                in_math = not in_math
                i += 2
                continue
            in_math = not in_math
        elif ch == "{" and not (i > 0 and text[i - 1] == "\\"):
            depth += 1
        elif ch == "}" and not (i > 0 and text[i - 1] == "\\"):
            depth -= 1
            if depth < 0:
                return False
        i += 1
    return depth == 0 and not in_math


def _render(output: Path) -> int:
    bindings = json.loads((SUP / "candidate-source-bindings.json").read_text(encoding="utf-8-sig"))
    pack_dir = output / "render-packs-v2"
    pack_dir.mkdir(parents=True, exist_ok=True)
    summary = {}
    issues = []
    total = 0
    for binding in bindings:
        before_path = binding["source_path"]
        cand_rel = binding["path"]
        cand = ROOT / cand_rel
        data = _transfer.read_bytes(cand, root=ROOT)
        if digest(data) != binding["raw_sha256"] or len(data) != binding["bytes"]:
            raise ValueError("candidate source changed: " + cand_rel)
        name = before_path.replace("/", "_").replace(".jsonl", "")
        parts = [f"# 新版渲染包 {name}\n", f"来源: {cand_rel}\n", f"raw_sha256: {binding['raw_sha256']}\n"]
        n = 0
        for line in data.decode("utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            rid = rec.get("id") or rec.get("problem_id")
            n += 1
            parts.append(f"\n### {rid}\n")
            for k in ("problem", "solution", "answer"):
                v = rec.get(k)
                if isinstance(v, str) and v:
                    if not latex_balanced(v):
                        issues.append({"id": rid, "field": k, "code": "latex_unbalanced"})
                    parts.append(f"**{k}** {v}\n")
            spec = rec.get("scene_spec")
            if isinstance(spec, dict):
                for i, s in enumerate(spec.get("objects") or []):
                    parts.append(f"**objects[{i}]** {s}\n")
                for i, s in enumerate(spec.get("steps") or []):
                    parts.append(f"**steps[{i}]** {s}\n")
        out = pack_dir / f"{name}.md"
        _transfer.fresh(out, "\n".join(parts).encode("utf-8"), root=output)
        summary[name] = {"records": n, "md_bytes": out.stat().st_size,
                         "source_sha256": binding["raw_sha256"]}
        total += n
        print(f"{name:40s} 记录={n:>4d} md={out.stat().st_size:>9d} B")
    report = {
        "schema": "render-packs-v2-v1",
        "note": "新版渲染包(candidate-sources为源);本包为MathJax渲染输入层,"
                "Manim场景渲染仍UNVERIFIED(需AppContainer证书+manim环境,生产门CLOSED)",
        "sources_bindings_verified": True,
        "total_records": total,
        "latex_balance_issues": issues,
        "summary": summary,
        "old_packs_not_valid_for_new_versions": True,
        "native_render_verdict": "UNVERIFIED",
    }
    rp = output / "render-packs-v2-report.json"
    _transfer.fresh(rp, (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8"), root=output)
    b = rp.read_bytes()
    print(f"\n总计 {total} 条;LaTeX平衡问题 {len(issues)} 条")
    print(f"报告: {rp.relative_to(ROOT)}  sha256={digest(b)}  bytes={len(b)}")
    return 1 if issues else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    if not args.execute:
        print(json.dumps({"status": "PLAN", "tool": 'render_packs_v2', "output": str(args.out) if args.out else None,
                          "writes": False, "historical_inputs": "READ_ONLY", "production": "CLOSED"}))
        return 3
    try:
        output = _fresh_output(args)
        return _render(output)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "FAILED", "detail": str(exc), "production": "CLOSED"}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
