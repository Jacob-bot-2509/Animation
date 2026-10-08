# IPv4 外部层级联合认定规则

用户于 2026-10-06 明确授权：接受“局域网 IPv4 受控证人 + 外部 IPv6 实锤 + 本机 IPv4 最强证据”联合认定，不再单独要求公网 IPv4 节点。该授权替代此前对 D1/D7 单独公网 IPv4 节点的要求；其他安全点仍逐项验收。

实现策略标识为 user-ipv4-joint-v1。通过时记为用户授权的 IPv4 联合推断，不能写成已直接测量公网 IPv4 投递。

| 点 | 局域网 IPv4 受控证人 | 外部 IPv6 实锤 | 本机 IPv4 最强证据 |
|---|---|---|---|
| D1：TCP IPv4 外部层级 | 独立 LAN 主机的 TCP IPv4 完整接收对照 | D2：真实外部受控 IPv6 TCP 接收对照 | D3：当前生产原生 AppContainer 的 TCP IPv4 回环接收对照 |
| D7：UDP IPv4 外部层级 | 独立 LAN 主机的 UDP IPv4 完整接收对照 | D8：真实外部受控 IPv6 UDP 接收对照 | D5：当前生产原生 AppContainer 的 UDP IPv4 回环接收对照 |

三个分量必须全部成立，TCP 与 UDP 分别核验。本机最强证据指当前受控接收器、直接原生网络调用、完整父 token/profile/ACL 与实现 SHA 绑定的 D3/D5；仅 Python 拦截、单个 10013、连通性或发包返回值均不足。D10–D13 继续各自核验，不能从此联合认定推导 DNS、非 Python、ICMP 或 HTTP API 已通过。

每个分量的 before/sandbox/after 是三个不同的 32 位十六进制 nonce。每条联合链九个 nonce 全部不同。相同协议、端点、载荷的宿主 before/after 必须各精确收到一次；不得收到 sandbox nonce，全部原始记录须归因。沙箱尝试后完整观察至少 20 秒；接收器完整结束、无错误。任一分量出现真实沙箱送达即 FAIL；不完整、无法解释或缺失材料不能 GREEN。

每个分量仍经 transport 重新核验：实际执行源码、命令、原始 stdout/stderr、退出码、父身份/生命周期、精确四根 ACL 回收、15 项当前实现/runtime SHA。原始证据只能新增，不能改写历史 JSON 或把旧 SHA 换成新 SHA。

外部 IPv6 必须属于独立受控接收者，且在发送主机原生 IPv6 接口前缀范围之外。发送端与目标同 /64 的校园 IPv6 主机始终归入 LAN，不能作为外部 IPv6 实锤。当前所报 2001:da8:2019:b282:c502:dd3f:3487:74fe 与训练机同 /64；其 LAN 身份不受公网地址外观影响。

## 机器可复验字段

在新的 sandbox-surface-native-v1 回执 cases.D1 / cases.D7 中使用：

~~~json
{
  "operation": "external_tcp_v4",
  "acceptance_basis": "user-ipv4-joint-v1",
  "components": {
    "lan_ipv4": "替换为实际 lan_peer case 对象",
    "external_ipv6": "替换为实际 external_tcp_v6 case 对象",
    "local_ipv4": "替换为实际 loopback_tcp_v4 case 对象"
  },
  "topology_evidence": {
    "path": "实际 topology.json 绝对路径",
    "sha256": "实际文件 SHA256"
  }
}
~~~

这是未验证模板，字符串占位符不能通过验收。D7 将三个 operation 分别换为 external_udp_v4、external_udp_v6、loopback_udp_v4；LAN 分量仍为 lan_peer，其 wire_protocol 为 udp。D1 的 LAN 分量 wire_protocol 为 tcp；LAN endpoint 为 IPv4，independent_lan_peer 为 true，仍须实际证据支持。

topology.json 和发送端接口 stdout 文件都存放在 reviews/codex-supervision/2026-10-06-all43-sandbox-repair 下的新唯一子目录；证据路径必须是普通文件，禁止链接或重解析路径。

topology.json 结构：

~~~json
{
  "schema": "ipv4-joint-topology-v1",
  "sender_host_id": "实际发送主机身份",
  "receiver_host_id": "实际外部接收主机身份",
  "controlled_receiver": true,
  "sender_ipv6": "实际发送 IPv6 地址",
  "receiver_ipv6": "与 external_ipv6.endpoint[0] 相同的规范 IPv6 地址",
  "sender_interfaces": {
    "path": "原生接口命令 stdout 文件的绝对路径",
    "sha256": "原始 stdout 文件 SHA256",
    "rc": 0,
    "stderr": "",
    "command": "Get-NetIPAddress -AddressFamily IPv6 | Select-Object IPAddress,PrefixLength | ConvertTo-Json -Compress"
  }
}
~~~

发送端运行上面 command 并完整保留实际 stdout/stderr、命令和 rc；stdout 中的 IPAddress/PrefixLength 是原生接口输出，不能自行缩小前缀。发送地址必须出现在输出中，目标不得处于任何已捕获接口前缀或发送地址所在 /64。另保留两端身份、接口/路由、受控接收程序身份及完整 JSONL/summary，以供独立真实性审核。

工具默认 --ipv4-evidence joint；--plan 展示该规则而不启动探针。选择 direct 仍可采集直接 IPv4 路径，但不能将它重新列为默认必需资源。采集脚本输出完整不等于通过；它不会自动生成缺失的 LAN/外部 IPv6 分量，也不会签发生产证书。

旧版 16 项兼容入口从已完整复验的 43 点 D1 联合 envelope 重新核验 IPv4 TCP；不会另要求公网 IPv4 节点。旧原生记录中的实际 IPv4 连接/送达不能被新规则掩盖。43 点任何一项未 GREEN 时，生产门禁仍 CLOSED。
