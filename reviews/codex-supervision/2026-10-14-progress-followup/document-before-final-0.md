# Animation Model Training v0.5.0

发布日期：2026-10-13
发布类型：双端实验突破与自动化版（Pre-release）

本版本同步 10-09 至 10-13 的进展：沙箱双端实验 LAN 轮首次完整成立并获 Codex 独立裁决通过、证人工具链 v3 防错交付、外部 IPv6 缺口延期补做（用户直接授权）、证据采集与对账自动化（第二三层）设计并交付三工具、OneDrive 材料通道接入准备。生产门禁保持 CLOSED，训练未启动。

## 版本可重现性

2026-10-14 独立核对：71c2d4c 仅删除两个运行时锁的 Git 跟踪记录，8b717ff 仅修改本发布说明。tools/witness_transfer_common.py、witness_pack.py、witness_consumer.py、witness_registered_adapter.py、tests/test_witness_automation.py、configs/witness_automation.example.json 六份交付文件仍未被 Git 跟踪。它们的当前字节与已验收归档一致，但当前提交单独 checkout 不能重现该工具交付；本版本说明限定工作区与冻结归档的交付范围，不能宣称源码已全部收拢入提交。

[实现与完整 SHA](archives/reviews/codex-supervision/2026-10-13-witness-automation-implementation/FIX_REPORT.md) · [接入步骤](archives/reviews/codex-supervision/2026-10-13-witness-automation-implementation/RUNBOOK.md)

## 本次交付

### 沙箱双端实验（本轮核心突破）

- **LAN 轮 lan-2026-10-13-a 首次完整成立**：证人机 v3 接收器（SHA 02d781bc…）具体绑定 192.168.137.1（Windows 热点双机同网），接收端四份原始 payload 记录与发送端宿主 before/after TCP+UDP 四个 nonce 逐一精确对应；沙箱 TCP 探针 os_denied（WinError 10013，socket 层被拒）；沙箱 UDP 本地 send 成功但证人零收到（因果机制未建立，不下"静默拦截实锤"结论）。
- **Codex 独立裁决：PASS_BOUND_LAN_D9_TCP_UDP_REGISTERED_WINDOW_ONLY**——对提交原件只读注册回放逐项比对：宿主 nonce 对应、观察窗完整、沙箱 nonce 未收到、进程启动调用 0。TCP/UDP 实际代码点位为 D9；D1/D7 仍缺联合 IPv6 依赖，不伪标绿。
- **IPv6（D2/D8）延期补做**：用户 2026-10-13 在 Codex 会话直接授权——现阶段如实 GAP 记账、不阻塞训练准备；等未来有可达公网 IPv6 证人时补做。
- 此前 LAN-a/b/c 与 v6 轮次的原始日志和诊断结论保留为历史证据。已观察到通配绑定、健康对照缺失与通路诊断失败；跨网段路由、客户端隔离、防火墙等原因仍未逐项建立，不能写成已经定位并排除。新 LAN 成立不追溯改变旧轮次资格。

### 证人工具链 v3 防错（witness-input-hardening）

- v3 接收器强制拒绝通配/回环/多播绑定；start_witness_capture.ps1 一键采集（五原件 + Base64 + process-exit.json 父进程回执，退出码与命令/轮次/进程哈希绑定）；inspect_witness_evidence.py 严格只读预检（禁止手填 rc）；驱动对账强制 --receiver-capture。
- 本地验证：接收器 12 项、驱动/检查器 45 项、启动器 10 项绑定复测、回环 IPv4/IPv6 自检 rc0、无效绑定 rc2 拒绝。

### 证据自动化（第二三层，OneDrive 通道）

- 设计稿 DESIGN.md（SHA 10d64d49…，32 项本地检查通过）。
- 三工具交付：witness_pack / witness_consumer / witness_registered_adapter + 公共模块，28 项回归全过（损坏包、缺 stderr、坏 rc 形状、ZIP 穿越与重复、并发锁、冲突幂等、崩溃恢复均实测）。
- 云盘选型：**OneDrive**（用户拍板）。配置默认 active=false；接入验证需提供证人 capture_root/sync_root、训练机 sync_root 与共享权限，先一次性验证材料通道再启用后台 watch。
- 红线：探针发射与采集启动仍归用户授权 + 本侧执行，Codex 不发射。

### 训练准备（无变化，口径继承 v0.4.0）

- configs/hp_sweep.json 中仅 center-confirmed 候选记录为 CONFIRMED、NOT_RUN_YET（r16/α32、LR 1/5000、cosine、batch 2×4、seq 2048、epochs 6、NF4 双量化）；其余三候选仍为 PROPOSED，试训计划为 PLANNED_NOT_RUN。configs/train_loop.example.json 是另一份 r8/α16 的 PROPOSED 模板，不能混同为已确认配置或已运行记录。
- 历史方案 A 及 holdout 391 条候选的训练流程仅作为计划记录。本轮在 Codex 会话直接确认的是训练准备与 IPv6 延期；历史文档中的开训声明不能替代本轮直接授权、实际配置绑定和训练门禁。试训与全量训练均未由本次审查放行。

## 状态与边界

- LAN 双端证据：PASS_BOUND_LAN_D9_TCP_UDP_REGISTERED_WINDOW_ONLY（仅该登记窗口内）；D1/D7 联合 IPv6 依赖仍缺；D2/D8 GAP（用户授权延期）。
- production=CLOSED、未发全 43 点/全局/正式开训许可；"训练准备"授权不等于开训。
- 全局语义隔离 NOT_ESTABLISHED、概念动画 NOT_EVALUATED、最小字形高度未认证。
- 本版本不是训练完成或生产就绪版本。

## 下一步

1. 自动化接入验证：确认两端 OneDrive 共享材料目录与各自权限 → 提供证人 capture_root/sync_root、训练机 sync_root 及 Python 环境 → 一次性材料通道验证 → 验收通过后启用隐藏后台 watch。账号接入方式尚未核验，不能预设两机使用同一账号。
2. 训练准备：数据构建（seq 2048 逐条校验）、冻结数据/配置绑定、门禁检查与试训方案准备；获得正式开训的直接授权并满足相应门禁后，才执行试训、holdout 泄漏检测、用户动画审阅与后续训练。
3. IPv6 补做：待未来可达公网 IPv6 证人出现。
