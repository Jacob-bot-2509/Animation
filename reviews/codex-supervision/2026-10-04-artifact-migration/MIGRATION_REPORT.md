# 任务产物迁移完成

2026-10-04，UTC+8。用户明确要求以后统一写入 Animation-Model-Training，并将此前 Codex 在 code 写的文件全部搬入该项目。

**已移动完整监督产物目录：5,030 个文件，184,900,115 字节，包含隐藏文件。移动后每个文件的长度及 SHA256 与迁移前清单完全匹配。旧 D:/code/output/claude-supervision 及空 output 目录均已移除。**

## 新位置与常用入口

旧前缀 D:/code/output/claude-supervision 对应新前缀 D:/Animation-Model-Training/reviews/codex-supervision/history-from-code；相对后缀不变。

- [最新本机回环加固报告](../history-from-code/network-core-hardening-2026-10-04/FIX_REPORT.md)
- [原 progress-v2 监督报告](../history-from-code/progress-v2-2026-10-04/SUPERVISION_REPORT.md)
- [原 progress 监督报告](../history-from-code/progress-2026-10-04/SUPERVISION_REPORT.md)
- [原沙箱修复报告](../history-from-code/sandbox-fix-2026-10-04/FIX_REPORT.md)
- [原 replay_a1_a2.py 快照](../history-from-code/progress-2026-10-04/snapshot/replay_a1_a2.py)
- [最新文件验收监督报告](../2026-10-04-acceptance-next/SUPERVISION_REPORT.md)

之后的新监督产物写入 reviews/codex-supervision/<日期-主题>/，已将用户要求保存到项目根 AGENTS.md，并建立 [记录索引](../README.md)。

## 校验与引用修正

[迁移前完整清单](before-manifest.json)、[移动后全量校验](move-verification.json)、[最终校验](final-verification.json)、[路径映射](path-mapping.json) 保存了全部文件数量、大小、相对路径与哈希。

校验完整移动后，修正了 7 份归档 Markdown 的旧落点引用；这些修改的原文单独备份。其余 5,023 份归档文件字节未变，包括全部原始 JSON、日志及源码快照。JSON 中记载的旧路径是当时实测来源，不重写历史证据；实际位置按迁移映射查找。

另修正了活动 network_isolation.py 的契约历史文档路径、两份支持脚本的 CODEX_RUNTIME 源目录字段，以及 2 份现行说明文档。活动代码通过 AST 比对确认仅路径字符串发生变化，已编译检查；没有变更验收逻辑、门禁、ACL 或启动原生测试。原生证据仍绑定迁移前测试时的源码哈希；仅路径变更后的当前文件哈希单独记录在 ../latest-live-file-hashes.json，历史收口证据不改写。

共 12 份引用/说明修改及其原文和前后 SHA，见 [引用修改记录](reference-updates.json)。

MathGuide 原有 .vscode/settings.json 修改仍保持原状，output 不再出现在该仓库未跟踪项中。已有 .bridge-poll 是 Claude/Copilot 的既有工具，非本次 Codex 产物，留在原项目；没有搬动项目原代码或其它人的文件。

已通过 AI Bridge 告知 Claude 新落点与运行时源映射；支持脚本后续修订以当前新 SHA 复验，生产门禁保持关闭。
