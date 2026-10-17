【第二轮审查：Codex 已修改 + 十题渲染 10/10】

① 归档分档：接受 archives/harness 归你，既有冻结件不迁移；Codex 报告继续写 archives/reviews/codex-supervision/，不启用 archives/codex（AGENTS 现行口径，未经用户直接改派；这是我的归档所有权决定）。

② 几何设计：结构可用。Codex 已在 geometry-layer-design.md 补 §五「与文字候选的合成边界」（`candidate_requires_dedicated_empty_canvas` 决定必须分场或模板 v4 组合，不能同屏拼贴）与 §六「保真硬约束」（等比例、逐题精确值、三维相机锁定）。另：提交 3eeed869 标题写「7 类模板」，正文与表格是 10 类，只记录不改历史提交。

③ 十题真实渲染（发现一个真错误）：AppContainer 试点下 v3 的 prob-042 失败——公式 `\text{正面}` 让 Manim 默认 LaTeX 报 `Unicode character 正 (U+6B63)`，状态 manim_failed。Codex 已修：新建 candidate-v2/records.jsonl，只改这一行（`\text{正面}`→`\text{heads}`，并在同一步注明 heads 为正面次数），其余 9 行逐字节不变。另修文字/公式紧贴：buff=0 → v4 的 0.12。重跑 10/10 成功，每题 45 帧 / 854×480 / 15fps / 约 40 秒；工件在 presentation-pipeline/runs/render-pilot/，manifest SHA256 ac262a6d80cbf6…，联系表 contact-sheet.png。

④ 复验：v4 模板 27 项、管线 14 项测试通过；场景审计 0 不符；管线重建 BUILT_PENDING_RENDER（10 包），render REFUSED，verify REVIEW_INCOMPLETE。

⑤ 交接要求：按 v4 + candidate-v2 继续；不要再改 v2/v3 模板字节；几何层实现前先读 §五/§六；渲染试点不是 43 项联合验收（network_isolated=false），不记 R/E/F、不解禁生产、不替代 10 份结论单。

归档：archives/reviews/codex-supervision/2026-10-17-presentation-pipeline-review/ROUND2_REPORT.md（SHA 见 metadata.report_sha256）。
