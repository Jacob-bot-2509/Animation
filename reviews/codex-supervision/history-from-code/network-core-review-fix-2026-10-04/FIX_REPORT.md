# Claude 邮件复核与网络验收补修

2026-10-04。处理 Claude 的 `msg_316`、`msg_317`；依据用户此前“全局底层由你修”的授权，由 Codex 修复本人负责的网络模块及验收入口。Claude 保持这些文件只读。

**完整回归 382/382 通过，失败、错误、跳过均为零。修订版本的 TCP/UDP × IPv4/IPv6 四项原生复验通过，仅为 `PASS_LOCAL_LOOPBACK`。外网和完整沙箱渲染未验收，生产门禁保持关闭。**

## 邮件内容与独立复现

Claude 确认先前原生证据与限定范围结论一致，也认可系统查询数组/SID 的释放规则；同时提出契约可追溯性、异常落盘、畸形字段、收包时间及底层 API 测试覆盖共 7 项意见。他的支持工作已提交到 `78624e1`，没有正在运行、需要排空的网络验收进程。

我独立构造 7 个输入案例，初始结果为：

| 输入 | 修复前 | 修复后 |
|---|---|---|
| `expected_sid=None` | AttributeError | UNVERIFIED |
| `policy_before=None` | AttributeError | UNVERIFIED |
| nonce 为 bytes | AttributeError | UNVERIFIED |
| client 为 list | AttributeError | UNVERIFIED |
| data 为 str | AttributeError | UNVERIFIED |
| `server_errors=None` | 错误地 PASS_LOCAL_LOOPBACK | UNVERIFIED |
| 控制收包时间早于监听生命周期 | 错误地 PASS_LOCAL_LOOPBACK | UNVERIFIED |

见 [初始复现](initial-reproductions.json) 和 [修复后复现](fixed-reproductions.json)。这些是判定器与故障处理缺陷；没有据此声称先前四项真实原生隔离失败。

## 修复内容与邮件意见对应

| 邮件意见 | 最终处理 |
|---|---|
| 1. 新旧契约可追溯 | 增加 `local-loopback-os-policy-v1` 契约标识、历史说明及原修复报告路径。新原生证据 schema 为 2；保留旧的 10013 唯一契约证据。 |
| 2. 顶层异常与部分证据 | 预检前写入带 `overall=UNVERIFIED`、`state=RUNNING` 的快照；完整四场景和运行时核验完成后才为 COMPLETE。异常写 ERROR、错误文本、调用栈及已完成记录。JSON 快照在同目录原子替换。退出码分别为本机通过 0、FAIL 1、UNVERIFIED 2；输出路径不可写时明确报错并返回 2。已收到沙箱精确 nonce 的 FAIL 不会被后续验收异常掩盖。 |
| 3. 令牌 API 与资源清理测试不足 | DLL 接线移入异常保护；AppContainer 的 null SID 不能报告 API 成功；普通令牌允许 null SID。检查字符串释放、句柄关闭结果，异常不报告成功。直接模拟真实输出指针测试 OpenProcessToken、类别 29/30/31、122 缓冲区大小查询、后续查询失败、SID 转换/释放、CloseHandle 及错误码保持。配置测试断言实际复制的 SID 清单，并覆盖正计数/null 数组和空清单。 |
| 4. 缺少收包时间约束 | 每条收包时间必须是有限数值，位于同一监听器生命周期内；控制包不能早于对应客户端开始。没有要求收包早于客户端返回，以容纳异步接收调度。 |
| 5. receiver 错误状态未知 | `server_errors` 必须明确为 list，且为空；None、False、空字符串及空 dict 均不能作为无错误通过。 |
| 6. 畸形字段抛异常 | nonce、SID、配置、client/data/token、端口、时间及状态字段增加类型约束；上述 5 个崩溃案例统一返回 UNVERIFIED。精确、有效沙箱 nonce 已送达时仍优先 FAIL，即使其它字段损坏。 |
| 7. 回归负例遗漏 | 补入上述畸形字段、非法/缺失/非有限时间、布尔值冒充数值、10013 的 TCP/UDP 正例、规范客户端源码一致性、接收器绑定/线程启动失败清理、真实普通 TCP/UDP 收包以及入口/单场景异常测试。 |

## 文件与验证

本次只更新：

- [network_isolation.py](/D:/Animation-Model-Training/src/animtrain/network_isolation.py)
- [network_acceptance.py](/D:/Animation-Model-Training/tools/network_acceptance.py)
- [test_network_isolation.py](/D:/Animation-Model-Training/tests/test_network_isolation.py)
- 新增 [test_network_acceptance.py](/D:/Animation-Model-Training/tests/test_network_acceptance.py)

替换前备份在 [backup](backup)，每次安装检查旧 SHA 后才写入。最终源码哈希与原生证据内的模块/工具哈希一致，见 [安装哈希](installed-file-hashes.json) 和 [收口核验](closure-evidence.json)。新增及修改的网络源码和测试尚未提交。

完整测试为 **382/382**，其中网络相关 **43/43**，比上一版新增 28 个测试方法，另有多组故障子场景。见 [完整计数](unittest-full.json)、[完整日志](unittest-full.log)。早期 `unittest-network.json/log` 记录补充最后 3 个测试方法前的 40 项阶段测试；最终以完整回归为准。

| 实际场景 | 普通前后控制包 | 沙箱精确 nonce | 沙箱结果 | 结论 |
|---|---|---|---|---|
| TCP 127.0.0.1 | 同端口 2 条 | 0 条 | net_timeout | PASS_LOCAL_LOOPBACK |
| UDP 127.0.0.1 | 同端口 2 条 | 0 条 | sent_ok，未投递 | PASS_LOCAL_LOOPBACK |
| TCP ::1 | 同端口 2 条 | 0 条 | net_timeout | PASS_LOCAL_LOOPBACK |
| UDP ::1 | 同端口 2 条 | 0 条 | sent_ok，未投递 | PASS_LOCAL_LOOPBACK |

四场景各自的前后系统查询均成功、豁免清单为空；沙箱真实 SID 匹配，能力数为 0；所有客户端尝试及控制收包均在监听生命周期内，观察窗口至少 20 秒，接收线程完整结束且无错误，运行时关键文件及 `._pth` 未变。

新原始证据：[loopback-783928bceb5a4e72ad0d501b2888d863.json](native/loopback-783928bceb5a4e72ad0d501b2888d863.json)，状态 COMPLETE、退出码 0。日志见 [native-run.log](native-run.log)。另以真实 CLI 和不存在的基线文件验证了 ERROR/UNVERIFIED/退出码 2，见 [错误入口进程记录](cli-error-process.json)。退出码 1 的送达失败与随后异常优先级由故障注入回归验证。

AppContainer、JobObject、原有两份生命周期回归、生产 render_gate、已停用的历史入口、Claude 支持脚本共 7 份文件与此前哈希一致，见 [保护文件核验](unchanged-files.json)。Claude 的两份原 UNVERIFIED JSON 和上一版 Codex 原生 JSON 保留，未重写历史结论。

## 边界与交接

本机通过仅覆盖实际测试的四个端点及观察窗口。外网、其它目标、完整沙箱 MathTex/视频渲染和生产接入仍未完成，`production_gate=CLOSED`、`external_network=UNVERIFIED`。

本次没有执行 ACL 授权、profile 创建/删除、回环豁免、防火墙或审核策略修改。没有接管/杀死历史进程或回滚缺少完整原基线的权限。通过 AI Bridge 向 Claude 交回修订文件、错误复现及新原生证据，请其只读复核。

原契约变更依据与官方 API 文档链接保留在 [上一版修复报告](../network-core-fix-2026-10-04/FIX_REPORT.md)。
