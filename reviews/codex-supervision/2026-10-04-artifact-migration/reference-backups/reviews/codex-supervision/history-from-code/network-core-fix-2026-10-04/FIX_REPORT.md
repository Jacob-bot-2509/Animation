# 全局网络隔离证据与验收机制修复

2026-10-04。用户要求全局底层问题由 Codex 接手；已通知 Claude 暂停修改对应文件，并保留既有证据。

**本机回环 TCP/UDP × IPv4/IPv6 四项原生验收通过，标签为 `PASS_LOCAL_LOOPBACK`。全套 354 项单元测试通过。外网与完整沙箱渲染未验收，生产门禁保持关闭。**

## 修了什么

| 文件 | 最终行为 |
|---|---|
| [network_isolation.py](/D:/Animation-Model-Training/src/animtrain/network_isolation.py) | 全局可复用的真实令牌身份查询、只读系统回环豁免查询、同端口接收器与证据判定。令牌检查类别 29/30/31，包含真实 SID 与能力数。 |
| [network_acceptance.py](/D:/Animation-Model-Training/tools/network_acceptance.py) | 四场景受限原生验收入口，复用已授权 runtime/work/profile；同一绑定端口依次运行普通前对照、沙箱探针和普通后对照，保存全部命令、随机 nonce、原始收包、时间、哈希及系统配置。 |
| [test_network_isolation.py](/D:/Animation-Model-Training/tests/test_network_isolation.py) | 15 个测试方法及多组负例；覆盖假通过风险、窗口/身份/配置失败，以及系统 API 数组/SID 内存所有权与失败清理。 |
| [isolation_acceptance.py](/D:/Animation-Model-Training/tools/isolation_acceptance.py) | 停用历史错误入口，退出码 2，给出新入口与未完成范围；不再执行类别 26 的错误令牌探针或给原 Python/.venv 添加权限。原文件与哈希已备份。 |

AppContainer 启动、JobObject、两份既有回归与生产门禁五份哈希仍匹配已验收基线；没有覆盖 Claude 的支持脚本、两份旧原生 JSON 或其他工作区改动。新增源码及测试尚未提交。

## 判定问题与新契约

此前普通控制确实送达，而沙箱 TCP 超时、UDP 发送成功但未投递。仅认可 WSAEACCES `10013` 的契约不能收口这些观测。我的独立原生重放确认了相同结果；Windows 的 `NetworkIsolationDiagnoseConnectFailureAndGetInfo` 在本机回环地址返回 `ERROR_SUCCESS`、`NETISO_ERROR_TYPE_NONE`，这不提供缺失网络 capability 的肯定证据，没有拿它当阻断通过条件。

新契约结合以下实际证据，给出限定范围的本机回环通过：

1. 系统 `NetworkIsolationGetAppContainerConfig` 查询在运行前后均成功，返回稳定的允许回环 SID 清单，测试 AppContainer 的 SID 未获豁免。
2. 沙箱内成功查询真实令牌类别 29/30/31：是 AppContainer、能力数为零、真实 SID 与预期一致。
3. 同一个绑定端口的普通前后对照都收到各自完整随机 nonce；接收线程无错误且完整退出。
4. 沙箱 nonce 在明确观察窗口内没有收到；后对照在沙箱完成后至少 20 秒才开始，所有尝试落在监听器生命周期内。
5. 独立运行时关键文件、._pth 隔离配置、客户端和解释器实际自哈希及路径校验通过，运行前后未变。

收包缺失本身不会通过。系统查询失败、豁免未知/存在/发生变化、SID 不符、能力非零、控制失败、接收错误、未知/短窗口或运行时不可信均为 `UNVERIFIED`。沙箱精确 nonce 送达优先 `FAIL`。TCP 报告已成功发送却无收包仍为 `UNVERIFIED`。

官方依据：[回环豁免查询及内存释放规则](https://learn.microsoft.com/en-us/windows/win32/api/netfw/nf-netfw-networkisolationgetappcontainerconfig)、[令牌信息类别](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-token_information_class)、[连接失败诊断接口](https://learn.microsoft.com/en-us/windows/win32/api/netfw/nf-netfw-networkisolationdiagnoseconnectfailureandgetinfo)。查询 API 返回允许发送 loopback 的 AppContainer SID 清单；返回的各 SID 和数组均由调用方按官方规则 `HeapFree`，转换得到的 SID 字符串用 `LocalFree`。

## 实际验证

| 场景 | 普通前后对照 | 沙箱 nonce | 系统配置与令牌 | 结论 |
|---|---|---|---|---|
| TCP 127.0.0.1 | 同端口两条完整 nonce | 未收到 | 配置查询成功、SID 匹配、能力 0 | PASS_LOCAL_LOOPBACK |
| UDP 127.0.0.1 | 同端口两条完整 nonce | 未收到 | 同上 | PASS_LOCAL_LOOPBACK |
| TCP ::1 | 同端口两条完整 nonce | 未收到 | 同上 | PASS_LOCAL_LOOPBACK |
| UDP ::1 | 同端口两条完整 nonce | 未收到 | 同上 | PASS_LOCAL_LOOPBACK |

实际前后系统豁免清单均为空，四场景各有且只有两条控制收包记录。接收线程均退出，运行时关键文件与 ._pth 未变化。完整原始记录见 [原生验收 JSON](native/loopback-1a3670144c604100a8afd797d290806f.json)，汇总及核心哈希、停用入口退出码核验见 [收口证据](closure-evidence.json)。

回归：[完整测试计数](unittest-full.json)、[完整日志](unittest-full.log)。结果 **354/354**，失败、错误、跳过均为零。其中新增 15 个测试方法包含多个故障子场景。停用旧入口另用独立进程验证返回 2，没有执行其原权限授权路径。

初始原生诊断对照保留在 [诊断原型结果](native-diagnostic-prototype.json)。Claude 原先的两份 `UNVERIFIED` 证据保留原样；它们遵循旧的 WSAEACCES 唯一契约，本报告的新结论使用额外系统配置与同端口前后对照证据，不重写历史结论。

复验命令：

```powershell
D:\Animation-Model-Training\.venv\Scripts\python.exe -B D:\Animation-Model-Training\tools\network_acceptance.py --baseline-evidence D:\Animation-Model-Training\reviews\2026-10-04-acceptance-support\net-evidence\network-accept-results-acd319b3f814.json --output D:\code\output\claude-supervision\network-core-fix-2026-10-04\native
```

每次证据使用独立 run_id；工具复用先前已授权的隔离运行时和工作目录，不执行 ACL 授权、profile 创建/删除、loopback 豁免或防火墙修改。

## 范围与交接

通过仅覆盖实际测试的本机回环端点和窗口，不能推导外网、其它目标或完整生产隔离通过。外网 TCP、完整沙箱 MathTex/视频渲染及生产接入仍需独立验收。没有盲目回滚缺少原始完整基线的历史工具链 ACL。

已通过 AI Bridge `msg_315` 将最终代码、证据、新契约及边界交给 Claude，只读复核；根模块、工具与测试仍由 Codex 负责。旧源码备份见 [历史入口原文件](legacy-isolation-acceptance-backup.py) 与 [原始哈希](legacy-baseline-hash.json)。
