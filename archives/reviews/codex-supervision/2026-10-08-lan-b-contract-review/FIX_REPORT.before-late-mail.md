# LAN-b 协议核验与预测试工具修复

源邮件：msg_1791473707558_770。  
实验：lan-2026-10-08-b / remote-aefc74dd86f74ab0bbbca13e1ddfc7e6。  
当前实验裁决：NEEDS_EVIDENCE；工具修复资格：REPAIRED_PASS_LOCAL_PRETEST_DIAGNOSTICS。

Codex 已修改 tools/host_pretest_witness.py，并新增 tests/test_host_pretest_witness.py。原工具将连接超时10060标为PATH_ALIVE，是实际诊断错误；也将耗时舍入到一位小数，丢失精度。修复后分别输出 LOCAL_CONNECT_COMPLETED、CONNECTION_REFUSED、TIMEOUT_UNCONFIRMED、SOCKET_ERROR；任何状态均不认证受控证人收到数据。耗时记录整数 elapsed_ns 与约分后的 elapsed_ms_exact，异常路径关闭套接字，UDP 短发送不会标为成功，输出为有效 JSON 并明确 DIAGNOSTIC_ONLY / qualification=NOT_ESTABLISHED。

源码版本：
- 修改前预测试 SHA256：5e0704205b5878e37d615bd089e35dcc835800e5288d42d5572be3013d76b580。
- 修改后预测试 SHA256：7b0d1df0616222d6a73dab3cffcb81c2deb9de061f9af4184b7d7f60db6e8bc6。
- 新测试 SHA256：3f9a9541d38f3402049c004e8ad1fee39f09a5b8403fad5dfbb60e7e164aa027。

独立复验的11项模拟回归全部通过，覆盖超时误判、拒绝与成功的证人资格边界、精确分数计时、套接字创建/设置/收发异常、UDP短发送及JSON输出。未运行修复后预测试去连接外部证人。

对 Claude 提出的协议疑点，已完成源码审阅及新具名本机联动验证：
1. 注册驱动 controls(before/after)将各协议的32字节nonce传给 send，TCP执行 connect→sendall→shutdown，UDP执行sendto。不存在“宿主对照正常情况下不携带nonce”的分支。
2. 接收器对TCP EOF调用finish，记录收到的完整数据；空连接也会产生一条bytes=0、exact_nonce=false的payload事件。该事件不能用于健康对照。
3. 本机IPv4/IPv6分别将注册驱动send直接连到原接收器源码：两组均记录TCP/UDP各before/after四个准确nonce，另各记录一个空TCP连接；每组records=5、实际接收函数rc=0，日志哈希及生命周期一致。本机联动资格仅为PASS_LOCAL_LOOPBACK_PROTOCOL_ONLY，不是证人端EXE或外部沙箱验收。

因此，当前证据不支持“驱动省略nonce”或“接收器按协议忽略空连接”这两种解释。仍不能仅靠宿主completed及相近耗时确认连到了受控证人进程；原驱动明确receiver_delivery_verified=false。中间转发、其他监听进程、时间/日志对应关系等只是待核查方向，本轮不确定零记录原因，也不指称已经证明某个网络因素。

LAN-b 独立材料核验：
- sender SHA256 c90b1f19eb8ad869e1435e93a62212a9d1362196e2bf8e0bc9212657d8ee43ff。
- JSONL SHA256 bd91036f16b1f34d18a51e7ca7f7edc502878792cfc76956577616f9aa34920c。
- summary SHA256 7c0a6154cb355953258f9add9369cffa60263753a09fc84dac66bda8119fa0ec。
- wl4.b64、wl4s.b64去掉明确BEGIN/END容器行后严格Base64解码，实际字节分别与JSONL、summary完全相同。容器文本不是数字证书，也不独立证明传输者身份。
- 发送侧15项实现、驱动前后版本和生成探针源都匹配当前原版。注册驱动和接收器未修改，实验原件保留。
- 接收端具体绑定172.31.31.250；摘要与日志哈希一致，但只有created/listening/closed，无payload。精确采集时长3000098873/10000000秒；宿主TCP before/after耗时分别8999/400与36327/2000毫秒，耗时不能认证接收者。
- 作者称rc=0有控制台出处，当前交付目录只有日志和摘要，本轮未取得该原始控制台出处。因此未把作者声称的0传作真实rc；只读预检明确指出缺四项健康对照与缺真实退出码来源。若后续交原生rc来源，可以关闭退出码缺项，但仍不能补出缺失的四项对照。

Claude 应使用本轮修复版预测试与限定结论继续工作，不重复修改Codex已完成部分。先提交实际预测试命令/完整输出和证人rc控制台出处，并核对实际监听进程、端点、原日志对应及监听窗口；后续轮次按用户安排，保留旧轮失败证据，新轮nonce真实入账后再对账。远端接收器既有自检可用于诊断其运行实例，不能替代双端四项对照。不要为通过而改旧字段或仅凭本机联动签远端通过。

本轮归档包含前后源码、真实11项回归、两组本机原始日志、协议复现脚本、实验字节副本、Base64载体、独立版本/精确时长核验、源邮件与真实交接回执。production=CLOSED，全局隔离NOT_ESTABLISHED，原生沙箱UNVERIFIED；数学与公式既有完成版未改变。
