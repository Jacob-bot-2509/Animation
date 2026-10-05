"""盘点 codex-repair-v1 的问题现场(只读):公式内中文的具体上下文、
scene_spec.steps 前缀缺失样例。"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
CJK = re.compile(r"[\u4e00-\u9fff]")
TEXT_CJK = re.compile(r"\\text\{([^}]*[\u4e00-\u9fff][^}]*)\}")


def main() -> int:
    files = sorted(DRAFTS.glob("batch-*/draft-codex-repair-v1.jsonl"))
    # 1) 公式内中文:所有行所有字段
    print("== 公式内中文 \text{...} 出现处 ==")
    for p in files:
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            for f in ("problem", "solution", "answer"):
                t = r.get(f, "")
                for m in TEXT_CJK.finditer(t):
                    s = max(0, m.start() - 40)
                    print(f"{p.parent.name}/{r['id']} [{f}]: ...{t[s:m.end()+20]}...")
            spec = r.get("scene_spec", {})
            for k in ("objects", "steps"):
                for item in spec.get(k, []):
                    for m in TEXT_CJK.finditer(item):
                        s = max(0, m.start() - 30)
                        print(f"{p.parent.name}/{r['id']} [scene.{k}]: ...{item[s:m.end()+20]}...")
    # 2) 前缀缺失统计与样例
    print("\n== scene_spec.steps 前缀统计 ==")
    no_prefix = []
    for p in files:
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            steps = r.get("scene_spec", {}).get("steps", [])
            for i, s in enumerate(steps):
                if not s.startswith(f"第{i+1}步"):
                    no_prefix.append((p.parent.name, r["id"], i + 1, s[:50]))
    print("缺失前缀条数:", len(no_prefix))
    for b, qid, n, s in no_prefix[:12]:
        print(f"  {b}/{qid} step{n}: {s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
