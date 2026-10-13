# 网络验收第一版：复核不通过，已通知 Claude 修订

2026-10-04。本次继续监督 Claude Code 的网络验收阶段，并独立核对源码及判定。收到 Claude 的进度邮件 `msg_307`，随后发送修订审查 `msg_308`。审查固定源码 SHA-256：`3e9c8a0b3cad5d64e7d72926000b4b7df127df3ec2415134c64704394bfe020b`。

**第一版网络验收工具尚不能可靠出具结论。当前没有网络原生验收结果；没有把工具的假通过判定当成真实隔离击穿或真实隔离成功。生产门禁继续关闭。**

## 独立复验发现

| 问题 | 固定源码位置 | 影响与要求 |
|---|---|---|
| 令牌能力查询类别错误 | `reviewed-network-source.py:172` | 使用类别 2 的 TokenGroups，不能据此证明能力数为零。应检查类别 30 的 TokenCapabilities，记录 API 是否成功和 GroupCount。 |
| 异常或未知探针可能 PASS | `reviewed-network-source.py:71` | 未检查沙箱是否启动、退出码及服务端完整状态。合成的退出码非零、未启动、收包未知、服务端错误四种输入均被判 PASS。 |
| 成功发送后无包直接 PASS | `reviewed-network-source.py:95` | TCP/UDP 的 sent_ok 都被放行。无法解释的未投递应 UNVERIFIED；明确收包应 FAIL；本阶段只在明确拒绝及完整可靠观测下判阻断通过。 |
| 已送达被控制失败掩盖 | `reviewed-network-source.py:71` | 服务端确实收到该次沙箱 nonce 时，即使控制失败也应 FAIL。当前返回 UNVERIFIED。 |
| 原始字节无法写入 JSON | `reviewed-network-source.py:368`、`:479` | 接收结果包含 bytes；成功收包后 json.dumps 会抛 TypeError。应保留可回放的 hex/base64、长度及编码。 |
| 接收端及干净运行时证据不完整 | `reviewed-network-source.py:255`、`:292` | 补齐创建、绑定、监听、接收异常与 finally 关闭，记录接收线程完成和单调时间界限；保存副本 ._pth、实际解释器/socket 路径与关键源码哈希，支持无 shim 结论。 |

令牌类别核对依据：[Microsoft TOKEN_INFORMATION_CLASS 文档](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-token_information_class)。官方区分 TokenGroups 与 TokenCapabilities，后者返回包含能力的 TOKEN_GROUPS 结构。

独立 AST 测试的 10 个场景只有 **3/10** 满足预期；其中 6 个不可信输入被误判 PASS，1 个沙箱送达场景被控制失败掩盖。其余 3 个为有效阻断基线、拒连不能通过和令牌探针失败不能通过。另独立复现 bytes 序列化 TypeError。这里只执行固定源码中的纯判定函数和客户端语法编译，没有运行 main、创建网络服务器/客户端、AppContainer profile、进程或 ACL。

证据：[固定源码](reviewed-network-source.py)、[独立结果与六份源码哈希](independent-judgment-results.json)、[可复用判定检查](check_network_judgment.py)。运行命令：

```powershell
D:\Animation-Model-Training\.venv\Scripts\python.exe -B D:\code\output\claude-supervision\network-review-2026-10-04\check_network_judgment.py
```

脚本退出码 1 表示严格预期未全部满足，不表示实际网络隔离已经失败。

## 核心边界和下一步

本轮确认 AppContainer、JobObject 和两份回归文件四份哈希均与既有修复基线一致，render_gate.py 哈希仍为 `7b6a6da10498991f4bd3e7a667195b657a92f610af7fd457988393b24677b026`。上一阶段继承句柄和进程树修复结论不变，见 [上一阶段收口报告](../closure-check-2026-10-04/SUPERVISION_REPORT.md)。

Claude 继续仅负责支持目录里的网络脚本与新证据；要求先修订判定、能力查询、结果序列化及负例，再回传供复核。运行时使用独立副本，新增 ACL 限定副本和工作目录；禁止修改原工具链权限、loopback 豁免、防火墙和 C 系统文件。未准许以当前第一版出具通过结论。

本机 TCP/UDP/IPv6 原生验收、外网 TCP 以及完整沙箱 MathTex/视频渲染仍待完成。
