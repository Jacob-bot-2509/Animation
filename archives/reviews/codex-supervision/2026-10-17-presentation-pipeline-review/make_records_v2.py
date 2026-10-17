"""生成 records v2:仅修正 prob-042 公式里的 CJK(默认 LaTeX 模板不支持 \text{正面})。

其余记录逐字节保留;只替换 prob-042 那一行,并写 PATCH.md 说明。
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(r"D:\Animation-Model-Training")
SRC = ROOT / ("archives/reviews/codex-supervision/2026-10-17-first-batch-exact-math-review"
              "/candidate/records.jsonl")
DST_DIR = ROOT / ("archives/reviews/codex-supervision/2026-10-17-first-batch-exact-math-review"
                  "/candidate-v2")
DST = DST_DIR / "records.jsonl"
OLD_MATH = r"\frac{\#\text{正面}}{n}"
NEW_MATH = r"\frac{\#\text{heads}}{n}"

lines = SRC.read_text(encoding="utf-8").splitlines()
out, changed = [], 0
for line in lines:
    if not line.strip():
        out.append(line)
        continue
    rec = json.loads(line)
    if rec.get("id") == "prob-042":
        spec = rec.get("scene_spec") or {}
        steps = spec.get("steps") or []
        hits = 0
        for i, step in enumerate(steps):
            if OLD_MATH in step:
                steps[i] = step.replace(OLD_MATH, NEW_MATH).replace(
                    "；没有实际序列时只显示公式",
                    "（$\\text{heads}$ 为正面次数）；没有实际序列时只显示公式")
                hits += 1
        if hits != 1:
            raise SystemExit(f"prob-042 expected 1 CJK formula, got {hits}")
        line = json.dumps(rec, ensure_ascii=False)
        changed += 1
    out.append(line)

DST_DIR.mkdir(parents=True, exist_ok=True)
DST.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
(DST_DIR / "PATCH.md").write_text(
    "# records v2 补丁(Codex, 2026-10-17)\n\n"
    "原因:prob-042 的公式 `$F_n=\\frac{\\#\\text{正面}}{n}$` 把中文放进 MathTex;\n"
    "Manim 默认 LaTeX 模板(english babel,无 CJK 支持)报 `! LaTeX Error: Unicode character 正 (U+6B63)`,\n"
    "该题在 AppContainer 试点中真实失败(work 目录见 render-pilot results.json)。\n\n"
    f"- 源:`{SRC.relative_to(ROOT).as_posix()}`\n"
    f"- 源 SHA256:{sha(SRC)}\n"
    f"- 本文件 SHA256:{sha(DST)}\n"
    f"- 改动行数:{changed}(仅 prob-042)\n"
    "- 改法:`\\text{正面}` → `\\text{heads}` 并在同一步注明“heads 为正面次数”;其余记录逐字节保留。\n"
    "- 不影响题目、解答或答案,只改场景文字里的公式写法。\n",
    encoding="utf-8")
print("wrote", DST, "changed", changed, "sha", sha(DST))
