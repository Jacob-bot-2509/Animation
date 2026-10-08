# 当前后续复核

本轮修复四个训练题的同核心／嵌入评测子任务，保留题号与761记录；757条完整记录继承不变。数学与场景文字、签名对应合格，46项精确符号检查及6项一般性证明通过。签名／深层工具46项回归、真实公式生成器15项回归，共61项通过。

原162次呈现实际均调用常量空MathTex，公式资格不合格。生成器修复后，7条当前记录的180个按题去重公式条目真实编译通过；其余156条当前记录已交Claude Code完整重渲。视觉、全局语义隔离及原生隔离未据此通过，production=CLOSED，未发PASS_CORE_SCOPE。双端实验不由Codex执行或验收。

[本轮修复与资格报告](../2026-10-07-deep-isolation-followup/FIX_REPORT.md) · [当前核心](../2026-10-07-deep-isolation-followup/effective-core-v3/current-index.json) · [精确题文](../2026-10-07-deep-isolation-followup/effective-core-v3/mathematical-before-after.json) · [重渲清单](../2026-10-07-deep-isolation-followup/native-resubmission-requirements.json) · [归档复验](deep-delivery-verification.json)

[上一轮761签名与c18改写](../2026-10-07-semantic-signature-supervision/FIX_REPORT.md) 及 [初次完整核心数学复核](current-core/FIX_REPORT.md) 为冻结父版历史。只读观察器已更新源码／回执范围并隐藏恢复，仅记录，不自动审查或放行。
