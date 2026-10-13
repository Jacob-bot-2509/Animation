# 定时邮件核验与监管 README 编码修复

本批 run-765d4e3452eb4c39a9667eb3ceb89590 只有 msg_1791467486033_755。已按调度器实际 message_hash 算法核对 packet、原始 messages 快照与上一轮收件回执，完全一致。本批此前未 ACK。

该邮件已在 2026-10-08-dual-endpoint-supervision 归档审阅，并收到实际回信 msg_1791467606465_756。独立核对其 29 件冻结材料、当前 sender 原字节及采集器源码哈希，继承完全相同版本的具名发送侧核验和 66 项本地回归，不重跑实验或未变化测试。邮件是状态材料，不能代替用户授权。本定时回合没有启动或验收双端实验，也不重装调度器。

msg_755 的发送侧 complete=true 与 UNVERIFIED 一致；TCP Win10013、UDP sent 不构成完整双端通过。LAN 尚缺原始 witness_new_01.jsonl、同名 witness_new_01.jsonl.summary.json、真实退出码与对应对账回执；外部 IPv6 新轮也须完整的发送、接收和拓扑证据。当前判定 NEEDS_EVIDENCE，生产 CLOSED。用户前一轮直接授权的监管结果可以作为既有具名材料继承，不把旧实验结论扩大。

本批读取观察器工作说明时，发现 Codex 上一轮在 README.md 追加的中文段落被编码成问号。Codex 已实际修改 reviews/codex-supervision/2026-10-04-live-watch/README.md，仅用 UTF-8 恢复该末尾段落；前面历史原字节完全保留。原乱码全文保存在本目录 README.before.md，修正全文在 README.after.md；已冻结的旧归档不改。该问题出在 Codex 上轮追加操作，本轮修正。

独立检查：当前 README 的前缀与原历史快照字节相同；修复段按 UTF-8 解码与明确文字逐字相同，没有问号替代；报告链接对应真实冻结报告；此前 sender、采集器、调度器源码及旧归档保持原哈希。仅给本地工作说明修复合格，不改变原生沙箱、双端、整体语义隔离或生产资格。

本批按 NEEDS_EVIDENCE 记录邮件现状，并以实际回信告知 Codex 已修文件、复验和合格范围，要求 Claude 按已修工作说明继续后续授权工作。RESULT.json 全量覆盖一条邮件；使用原 mail_watch.py ack 确认本批。新的接收材料应由新邮件触发新的独立审阅，不覆写已有归档。
