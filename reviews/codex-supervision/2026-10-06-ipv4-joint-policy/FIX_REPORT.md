# IPv4 联合认定已接入，完整验收仍待证据

用户明确授权 user-ipv4-joint-v1：IPv4 外部层级接受“局域网 IPv4 受控证人 + 外部 IPv6 实锤 + 本机 IPv4 最强证据”，不再单独要求公网 IPv4 节点。已同步修正 43 点重算、16 项兼容入口及生产证书检查；采集工具默认 joint，并提供无执行的 --plan。

D1 使用 LAN IPv4 TCP + 外部 IPv6 TCP（D2）+ 本机 IPv4 TCP（D3）；D7 使用对应 UDP 三项（D8/D5）。通过结论明确标为用户授权的联合推断，不伪称公网 IPv4 直接实测。三项完整成立才可 GREEN，任一实际沙箱送达即 FAIL；同 /64 校园 IPv6 不能作为外部证据。详细字段与采集要求见 [POLICY.md](POLICY.md)。

82 项相关回归通过，其中 26 项新增联合认定测试覆盖缺项、协议/地址族混用、接口/拓扑 SHA 篡改、同网段 IPv6、nonce 复用、完整观察窗口、原生送达与旧兼容入口。测试中的联合网络夹具是模拟数据，不能代替外部/LAN 原生验收。

更改了三个已绑定验证源文件后，另行运行 8 个主原生容器作业及真实 Windows 宿主故障/锁夹具；已保留新的源码、命令、完整 stdout/stderr、父 token/profile/精确四根 ACL 恢复及 15 项实现/runtime 绑定。独立重算当前 **30 GREEN、0 FAIL、2 PARTIAL、11 GAP**。原生控制器 rc=3 表示全表未齐，符合预期。

新主原始回执：
../2026-10-06-all43-sandbox-repair/surface-raw-6367b72967e04ed5b36dc234764e209a.json
SHA256：e9185cd8b43fa090d4e885dc90dd7df7906a9e79d5c2e86cf486ba53f0f53464。

另一次当前绑定的匿名管道原生补测通过，两端 query 均被 STATUS_INVALID_HANDLE（−1073741816）拒绝；宿主 before/after 同夹具健康，不能替代跨用户管道。新回执 anonymous-pipe-74cf1a9510ab4a13ad3c58c4320c1082.json 保存在同一 all43 证据目录。

D1/D7 的三项联合材料尚未齐全，当前仍 GAP。D1/D2/D7/D8/D9/D10/D11/D12/D13/F5/F6 为 GAP，F2/F4 为 PARTIAL；接收器自测、策略修改或公共 IPv6 ping 不直接增加绿色计数。GREEN 仅涵盖注册夹具矩阵，E3 是文档验证。

旧原始回执、源码快照、签过的历史交付清单与证人 EXE 均保留原字节；新源码导致旧实现绑定失效，因此采用新原生回执，不给旧材料重签。本次自有 C 盘临时夹具已保全两个普通文件并逐个删除，再移除空目录；未递归删除、未访问系统文件。清理回执与当前状态另存，原始 cleanup-pending 字段不改写。

观察器新增本目录、联合认定测试和采集入口；旧 worker 35160 正常 STOP，新隐藏 worker 44260 已确认心跳。后台观察只记录，不能自动进行 AI 验收。

生产门禁 **CLOSED**，全 43 点未齐，无生产证书；未启动训练。Claude Code 已收到政策变更预告，最终交付通过 Bridge 回传，实际回执见 handoff-receipt.json。
