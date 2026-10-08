# 新采集与对账契约

实验日期按用户安排为 2026-10-08（北京时间）。本文仅为使用说明，没有启动探针或接收器。

1. 先确认不同主机上的已核验 witness_receiver_v2.exe/source，协议端口和显式地址族一致。记录完整 hostname、监听 literal、运行时长、程序 SHA。监听窗口应覆盖宿主前对照、整个沙箱作业、作业后至少 20 秒及后对照，接收器运行结束后提供真实 rc。
2. 发送端显式调用 tools/sandbox_external_test_driver.py 的 --execute-native、--bind 接收端literal、--round 新名称、--scope lan 或 external、--protocol both/tcp/udp。默认端口 UDP49001、TCP49002；观察窗默认21秒。只接受受控节点和注册路径。
3. 发送端生成唯一 sender.json、真实 route 和原生接口 raw streams，采集结果仍 UNVERIFIED。保存全部文件，不覆盖旧 RoundA。
4. 对端提供原始 v2 JSONL、原 summary 和真实 rc。原字节复制到注册根 reviews/codex-supervision/2026-10-06-all43-sandbox-repair 的唯一子目录；不编辑 summary 内原始路径，不把宿主 send 返回值当接收回执。
5. 使用独立对账参数 --reconcile sender.json --receiver-log 原JSONL --receiver-summary 原summary --receiver-rc 实际退出码；不得同时加 --execute-native。拒绝旧 sender schema，必须用新完整采集材料。
6. 对账通过仅覆盖该注册协议/层级；sandbox nonce 被接收立即 FAIL，材料缺失或生命周期不完整保持 PARTIAL。双协议分别验证；不生成 production certificate。

同 IPv6 /64 的校园设备是 LAN，不能写 scope=external。用户允许 IPv4 以“LAN IPv4受控证人 + 真正外部IPv6实锤 + 本机IPv4最强证据”联合认定，但各协议所需证据仍须完整。当前无合格双端对账回执，43点仍 30 GREEN / 2 PARTIAL / 11 GAP，生产 CLOSED。
