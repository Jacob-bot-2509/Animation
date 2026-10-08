# 当前公式交付与审阅进度（2026-10-08，本轮两处修复）

当前索引覆盖 **165条记录、633页，3840×2160**：[CURRENT_DELIVERY_INDEX.jsonl](../codex-supervision/2026-10-08-determinant-glyph-followup/CURRENT_DELIVERY_INDEX.jsonl)。SHA256：667278f661c3a0ca3f72b415a914d2cfc73845dad8f3987d31a38e82b32af715。

Codex已修复 eval-linalg-004-s3 的拆列行列式记号和 eval-linalg-002-s3 的三阶余子式展开方向标签。题目和正确答案保持不变。完整300条eval候选位于 [dataset_eval-final-candidate.jsonl](../codex-supervision/2026-10-08-determinant-glyph-followup/dataset_eval-final-candidate.jsonl)，保留上批3题修复，本轮仅再修2题。

当前记录版本由 [current-record-bindings.jsonl](../codex-supervision/2026-10-08-determinant-glyph-followup/current-record-bindings.jsonl) 唯一选择；761条记录、24个物理来源。先前候选与原始数据文件作为历史，不能越过当前绑定选择旧版本。完整复验与资格见 [FIX_REPORT.md](../codex-supervision/2026-10-08-determinant-glyph-followup/FIX_REPORT.md) 和 [final-independent-verification.json](../codex-supervision/2026-10-08-determinant-glyph-followup/final-independent-verification.json)。

- 本批核对8题的完整证明、实际查看32张原PNG及5张重渲PNG。当前32页合格。
- 累计实际逐页审阅 **296/633页**，尚余 **337页待审**：[current-unreviewed-pages.json](../codex-supervision/2026-10-08-determinant-glyph-followup/current-unreviewed-pages.json)。本批逐页结论与精确公式、PNG及记录摘要绑定。
- 当前633页尺寸、SHA、几何和源码公式绑定均验证；新5页独立解码核对视频像素，其他628页按相同公式、几何、PNG继承原像素证据。
- 当前完整公式页552张重新计算占用高度代理：最小92，第10百分位最近秩484/3，中位数219；1080高最小代理46。81张分片排除。这些值不能证明最小字形高度。
- **全部字形验收NOT_ESTABLISHED，最小字形高度NOT_CERTIFIED，概念动画NOT_EVALUATED，全局语义隔离NOT_ESTABLISHED，原生沙箱UNVERIFIED，生产CLOSED。**
- 本轮活动中文说明的编码已恢复。以下历史说明保留原字节，其旧数量和路径不得覆盖上面的当前交付。

