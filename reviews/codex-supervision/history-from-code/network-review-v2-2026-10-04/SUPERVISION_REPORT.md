# 当前进度：网络脚本已修至第二版，仍待补证

检查时间：2026-10-04 12:49（北京时间）。最新提交仍为 `f24e97edb8bc739675ff4c511df169954adfc7f0`。网络脚本已有工作区修订，未提交；第二版固定源码 SHA-256 为 `7bfdf66797bc1573f6993cb7e2203ddbb6a0dd2e90e8be33848c347d5ec100e1`。

**主要问题已有修正，但网络原生验收尚未执行出具结果，生产门禁保持关闭。** 当前支持目录未发现 `net-evidence/` 或复制的 `net-runtime/`；本轮多次检查 Codex 收件箱均没有新回信。已经向 Claude 发送状态询问 `msg_309` 和具体复核意见 `msg_310`，尚未收到回复。不据邮箱登记时间判断其是否正在运行。

## 已取得的进展

- 令牌能力查询从 TokenGroups 类别 2 改为 TokenCapabilities 类别 30，并记录 API 成功及返回大小。
- 沙箱未启动、退出码非零、接收未完结等主路径已加入拒绝通过的条件。
- TCP/UDP 成功发送而没有收包不再直接判 PASS；确实收到沙箱 nonce 时优先判 FAIL。
- 原始收包改用 hex、长度和显式编码，解决 bytes 直接写 JSON 的错误。独立执行 JSON 往返自检通过，并确认服务器快照可序列化。
- 我只加载纯函数后执行 Claude 的 15 项内置检查，结果 **15/15** 符合预期。这不代表真实网络验收通过。

## 独立复验仍有四项缺口

| 检查 | 当前结果 | 修订要求 |
|---|---|---|
| 接收状态为未知 `delivered=None` | 纯判定仍返回 PASS | 未知不能证明阻断，明确要求 `delivered is False`。当前执行包装一般生成 bool，此项是纯判定输入完整性问题。 |
| 沙箱服务端已超时关闭，随后才启动探针 | 用假时间、假线程完整调用 `_attempt`，仍返回 PASS | 记录并核对实际尝试处于有效监听窗口，检查启动时服务端状态；历史 listening=True 不足以证明当时有效。 |
| 客户端报告 socket 模块来自原工具链目录 | 用假客户端完整调用 `_attempt`，仍返回 PASS | 校验 socket 路径确实位于运行时副本；不能只存路径。哈希也不能只检查字符串非空，需一致性核验；检查 ._pth 的隔离配置。 |
| TCP accept 成功后 recv 抛出异常 | 服务 socket 关闭，但已接受的 conn 未关闭 | conn 与 srv 都须在 finally 中关闭，包括接收超时/异常分支。 |

本轮独立 13 项检查 **9/13** 满足预期，已向 Claude 提交这四项具体修法。前次 10 项检查和本次 13 项检查的数量不同，本次新增了执行包装和连接清理的故障注入。

所有独立测试均使用 AST 加载选定函数与假 I/O；没有创建真实网络 socket、原生进程、AppContainer profile 或修改 ACL。因此，结果证明验收工具仍有缺口，不表示原生网络隔离已击穿。

证据：[固定第二版源码](source-snapshot.py)、[独立故障记录及内置检查结果](independent-v2-results.json)、[可复用测试脚本](check_v2.py)。命令：

```powershell
D:\Animation-Model-Training\.venv\Scripts\python.exe -B D:\Animation-Model-Training\reviews\codex-supervision\history-from-code\network-review-v2-2026-10-04\check_v2.py
```

## 已核对的核心边界

- AppContainer 源码 SHA-256 仍为 `69a5f2bea26e72b1c9d42b8fd213e6222fdf710ab41c3ed3018e73f76916c01f`。
- JobObject 源码 SHA-256 仍为 `6c8c6875fd5bf7270f04347ab93fb57f4d4b13b4faeb970f0b636ced2f8ae44c`。
- 门禁源码 SHA-256 仍为 `7b6a6da10498991f4bd3e7a667195b657a92f610af7fd457988393b24677b026`。

已验收的继承句柄和进程树修复结论不变，见 [核心修复阶段收口报告](../closure-check-2026-10-04/SUPERVISION_REPORT.md)。第一版网络检查见 [上轮报告](../network-review-2026-10-04/SUPERVISION_REPORT.md)。

下一步仍是 Claude 在支持目录内补完这四项，复核后再执行本机 TCP/UDP/IPv6 原生收包正反对照。外网 TCP、完整沙箱 MathTex/视频渲染及生产接入均未完成，不开放门禁，也不需要重复跑未变化的核心全套测试。
