# LAN 新材料的限定说明

适用于 commit 7a444a67，round=lan-2026-10-13-a，sender run=remote-3a28dfd9dc96430a8ed0edb1989c3e76。

本说明仅记录提交文件一致性及报告边界，不是双端实验验收，不签发 D9、D1、D7 或全 43 点资格。

1. 当前原件含四个健康对照 payload：TCP before/after、UDP before/after，均与 sender 记录精确对应。原始接收日志有 7 个事件，summary.records=4，具体 endpoint 是 192.168.137.1 的 UDP 49001 和 TCP 49002。
2. 父回执、接收 run、当前 v3 EXE 哈希、启动器哈希和四份原始输出哈希一致。重新执行只读材料检查器返回 READY_FOR_REGISTERED_RECONCILIATION，无 finding，full_surface_accepted=false，production=CLOSED。这不是本轮实验准入结论。
3. 提交的 reconciled 文件把 TCP 和 UDP 均登记为 D9 / lan_peer，不是 D1 / D7。不能将两个 LAN 记录直接改签为外部 IPv4 项。
4. 提交记录中的 TCP 沙箱结果为 os_denied / winerror=10013，UDP 为本地 sent。接收日志中未见对应 sandbox nonce，只证明提交日志未记录该 payload；不能据此认定 UDP 的具体丢失位置或“静默拦截”机制。commit 标题中的该因果表述应按此限定说明读取，历史 commit 和原始记录不改写。
5. 邮件陈述“IPv6 已放弃”和“后续进入训练线”是待审材料，不改变用户授权或门禁。既有 IPv4 联合认定条件包含受控 LAN IPv4、真实外部 IPv6 和本机 IPv4 证据；单独 LAN 材料不自动满足整个联合条件。当前仍为原生沙箱 UNVERIFIED、全局隔离 NOT_ESTABLISHED、production=CLOSED。
6. 本次 decoder 源码中的内嵌材料有实际损坏，不能用于重建原件：summary 5992c73c… 与原件 96b0279f… 不同，stdout 6e4a8231… 与原件 872c9366… 不同且 JSON 无效，process-exit b4d4a2b3… 与原件 147bf8f4… 不同。完整证据见 decoder-independent-findings.json。Codex 已修复本地重建工具，提交的正确原件保持不动。
