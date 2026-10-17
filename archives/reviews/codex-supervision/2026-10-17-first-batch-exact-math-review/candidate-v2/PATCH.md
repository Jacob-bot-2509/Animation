# records v2 补丁(Codex, 2026-10-17)

原因:prob-042 的公式 `$F_n=\frac{\#\text{正面}}{n}$` 把中文放进 MathTex;
Manim 默认 LaTeX 模板(english babel,无 CJK 支持)报 `! LaTeX Error: Unicode character 正 (U+6B63)`,
该题在 AppContainer 试点中真实失败(work 目录见 render-pilot results.json)。

- 源:`archives/reviews/codex-supervision/2026-10-17-first-batch-exact-math-review/candidate/records.jsonl`
- 源 SHA256:f45865e22398cfac50d1c5d50377a4d404941aefa79e26b125d4f8d26a71883c
- 本文件 SHA256:e686ce7e8ac9c8c313d70cffdbecf6c140f044b27ab5f5966321ff61acd45246
- 改动行数:1(仅 prob-042)
- 改法:`\text{正面}` → `\text{heads}` 并在同一步注明“heads 为正面次数”;其余记录逐字节保留。
- 不影响题目、解答或答案,只改场景文字里的公式写法。
