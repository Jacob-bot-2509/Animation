# IPv6 双端实验(D2/D8)用具清单与步骤 Runbook

状态:PLAN_PREPARED_NOT_EXECUTION_AUTHORIZED(依据 Codex 871 与 NEW_ROUND_REQUIREMENTS.md)。
本文件是执行包;**开工须先过四道闸**(见二)。所有身份/地址/退出码未知时写 null/PENDING,不填希望值。

## 一、实验用具清单

### A. 证人机(第一道闸,你这边)
| 项 | 要求(Codex 口径) |
|---|---|
| 主机 | 与训练机**不同的物理/虚拟主机**;之前候选:WJW(OneDrive 已登录)/新电脑(成功 LAN 轮那台) |
| 公网 IPv6 | 具体**全局单播地址(GUA)+ PrefixLength + 路由**;GUA 字样不证明外部——要保留两端接口/前缀/路由/拓扑材料;check_scope 拒绝发送端任一接口前缀内目标,IPv6 还拒绝**同 /64**;证明不了外部就记 GAP |
| 端口 | v3 启动器 SERVE 固定 **UDP 49001、TCP 49002、300 秒**(改的话先核程序支持,不能只改手册) |
| OneDrive | 登录同一账号(Jacapo061010@outlook.com),sync_root=OneDrive\witness |
| kit | 拷入 kit 目录(在 OneDrive 之外),含 witness_receiver_v3.exe(预期 SHA 02d781bc22286b1e8417ddb119ec6b529e5a9101b1fad758a41a06fbc2eb44bf,**现场前后核验**)、start_witness_capture.ps1、inspect_witness_evidence.py、witness_pack.py(Codex 修复版) |

### B. 训练机(我这边)
- 四工具修复版(consumer SHA 5694391f…)、常驻 watch(现行)、configs/witness_automation.local.json
- sandbox_external_test_driver.py(SHA a02105a0…)作发送端驱动
- 发送端原始材料接口/路由/拓扑采集命令

### C. 参数与 nonce(铁律)
- 观察参数整数 21-90 秒;**post-attempt 实际窗口 ≥20 秒**(elapsed_ns≥20,000,000,000)
- 每协议 before/sandbox/after **三个唯一 32 位十六进制 nonce**;TCP+UDP 合计六个互异(将来 D1/D7 三组件合计九个互异)
- 两机 monotonic_ns **不能相减/排序**;跨机靠同轮身份+端点+nonce+原始接收事件关联

## 二、四道前置闸(缺一不开工)

1. **证人机公网 IPv6 条件**(你侧):GUA+前缀+路由+拓扑材料;非 ::、回环、链路本地、多播、发送端自己
2. **新根/固定源码绑定审查**(Codex 侧):现行 driver 的 REGISTERED_ROOT 仍是旧 all43 根,transport/verifier 也有固定根——**不能直接把新路径传旧脚本**;须先过"新根统一边界"审查(我的方案已 REPAIRED_PASS 设计层,真实改造未做)
3. **用户明确授权**(你):写明具名采集范围(哪台证人、哪些端点、什么探针),发给 Codex
4. **新轮身份先审后发**:round/capture_id/receiver_run_id/sender_run_id/nonce 全部新取,不复用 lan-2026-10-13-a;registry 七键审查+加载确认后才发布 .ready

## 三、完整步骤

### Phase 0:准备材料(现在可做)
1. 证人机:`ipconfig /all` 存 IPv6 地址/前缀/默认网关;`route print -6`;确认 OneDrive 登录与 sync 目录
2. 训练机:本机 IPv6 接口/路由采集存档(两端拓扑对照)
3. 新轮命名提案:round=`ipv6-YYYYMMDD-<x>`(1-64 ASCII 字母数字/下划线/连字符,首字符字母数字)
4. 把两端拓扑材料 + 新轮提案 + 你的授权文本一起发 Codex 审查
5. 同时等新根/工具版本审查结论(871 §5)

### Phase 1:获授权后启动(Codex 不发射,全部我执行)
1. 证人机:现场核验 witness_receiver_v3.exe SHA → 按获准计划启动 SERVE(监听 UDP 49001/TCP 49002/300 秒)
2. 训练机:跑 sandbox_external_test_driver 的 IPv6 external 用例:
   - TCP:before nonce 健康对照 → sandbox 内发 TCP nonce → after nonce 健康对照
   - UDP:同上独立三 nonce(不能从 TCP 可达推 UDP 可达)
   - 每协议 post-attempt 观察 ≥20 秒
3. 采集:发送端原始接口/路由/拓扑、typed rc/原始流、源码实现前后绑定;证人侧五原件(receiver.jsonl、receiver.jsonl.summary.json、stdout.bin、stderr.bin、process-exit.json——**内部日志仍用 sandbox-witness-receiver-v2,不许手改 schema**;mode 必须 SERVE,SELFTEST 不算)

### Phase 2:打包回传(与昨晚 OneDrive 流程相同)
1. 证人机:pack 只打包已完成的具名 capture(严格五原件)→ stage → OneDrive sync 目录 → **.ready 最后发**
2. 训练机:watch 消费 → 验 SHA/限制/拒重解析点 → v3 预检 → 匹配**新 registry** → 注册对账 → 归档
3. registry 增项七键:round/receiver_capture_id/expected_receiver_run_id/sender_run_id/sender_path/sender_sha256/input_bindings(绑发送端 IPv6 接口 stdout/stderr、transport.work 下 scene.py/stdout.txt/stderr.txt + 本轮路由/拓扑原件)

### Phase 3:Codex 独立复核
- 逐协议限定:D2=external IPv6 TCP、D8=external IPv6 UDP,**分别通过才报告对应点**
- 旧 LAN D9 仅按已认可窗口继承,不冒充本轮新实测

### Phase 4:结果资格
- 单点对账不签 43 点证书;新 D2/D8 不自动改其他 GAP/F2/F4 PARTIAL
- 只有全部适用验收满足才另提证书候选

## 四、原物清单(交付时的最小集)

- 证人侧:五原件 + EXE 前后 SHA + 启动器记录(真实命令/身份/typed rc)
- 发送端:新 sender.json(实际 source/transport/scene.py/stdout/stderr、父 token/Job/profile/ACL/树终止证据、接口/路由/拓扑、typed rc、nonce、观察窗)
- 两端 before/after 健康对照:接收端逐字节看见 before→after,**且没有任何 sandbox nonce**;真实收到 sandbox nonce = FAIL

## 五、不做的事

- 不复用旧轮身份/nonce;不把旧回放当新原件
- 不编辑/重新序列化/补写原件;失败原件保留,不调参重放
- 不改 frozen 目录、不放宽 bound_path
- OneDrive 同步成功 ≠ 探针网络可达;REGISTERED_RECONCILIATION_COMPLETE ≠ 43 点证书

提交时间以 git 记录为准。
