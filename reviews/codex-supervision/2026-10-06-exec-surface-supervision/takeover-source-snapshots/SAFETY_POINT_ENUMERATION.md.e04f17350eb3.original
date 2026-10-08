# 沙箱全安全点枚举(exec_isolation 门禁 ③)

- 依据:用户裁决(2026-10-06)——**只有沙箱所有安全点检测为绿才解禁**;16 项有限范围测试不足以放行。
- 本文件是权威安全点清单:每个点标注 实现来源(代码) / 现有证据 / 状态。
- 状态定义:
  - 🟢 GREEN — 16 项联合验收内已独立重算通过(production-joint-independent-review-v2.json,16/16 PASS)
  - 🔴 GAP — 尚未有原生证据(需新增探针)
  - 🟡 PARTIAL — 只有部分证据(如仅 Python 层、仅 IPv4)

## A. 容器身份与 profile 生命周期

| # | 安全点 | 来源 | 状态 | 现有证据 |
|---|---|---|---|---|
| A1 | 每次 job 全新 UUID profile,不可复用 | private_profile.py `_profile_grants` | 🟢 | joint-review parent_evidence(profile_name 正则) |
| A2 | SID 有效且容器 token SID 与 profile SID 一致 | isolation_evidence.py `_parent` | 🟢 | 同上 |
| A3 | 容器 token is_appcontainer=True | 同上 | 🟢 | 同上 |
| A4 | capability_count == 0(无任何能力) | 同上 | 🟢 | 同上 |
| A5 | profile 专属存储目录 job 后删除 | 同上 | 🟢 | 同上(storage 不存在) |
| A6 | 临时 ACL 授权仅限 项目根 + D:\Python,拒绝符号链接/重解析点根 | private_profile.py `_profile_grants` | 🟢 | 同上(temporary_acl 4 项,restored) |
| A7 | ACL 授权 job 后回收(before==after,SHA 绑定) | 同上 | 🟢 | 同上 |
| A8 | 授权前根目录不存在该新 SID 的既有 ACE | 同上(`Fresh UUID SID already granted` 检查) | 🟢 | 同上(代码级强制) |
| A9 | ACL 编辑跨进程串行化(transport.lock) | isolated_profile | 🟢 | 代码级强制 |

## B. 进程与作业对象

| # | 安全点 | 来源 | 状态 | 现有证据 |
|---|---|---|---|---|
| B1 | 仅继承 stdio 句柄(挂起创建→分配 Job→恢复) | appcontainer.py run_appcontainer | 🟢 | P5 / joint review |
| B2 | 根进程退出 → 整树停止 | 同上 | 🟢 | root_exit_tree PASS |
| B3 | 超时 → 整树终止(含孙进程) | 同上 | 🟢 | timeout_tree PASS |
| B4 | 内存上限 2 GiB(64MiB 块,超限 rc17 拒绝) | isolation_evidence.judge memory_limit | 🟢 | memory_limit PASS |
| B5 | Job 分配失败不恢复子进程(fail-closed) | 生命周期单元测试 | 🟢 | tests/test_appcontainer_lifecycle.py |

## C. 文件系统边界

| # | 安全点 | 来源 | 状态 | 现有证据 |
|---|---|---|---|---|
| C1 | 项目外读拒绝 | 16 项 file_read_outside | 🟢 | PASS |
| C2 | 项目外写拒绝(含 marker 缺失复核) | file_write_outside | 🟢 | PASS |
| C3 | D:\Python 工具链写拒绝 | file_write_runtime | 🟢 | PASS |
| C4 | 跨 run 持久写拒绝 | cross_run_write / cross_run_cache_write | 🟢 | PASS |
| C5 | job 期间私有/受保护文件不变(before/after SHA) | 同上 | 🟢 | PASS |
| C6 | **授权目录内符号链接/挂载点逃逸** | probe-exe-ipc-fs-v1 | 🟢 | 2026-10-06 实测:junction **创建即被拒**(拒绝访问),写通道无从建立 |
| C7 | **外部文件删除**(DELETE 权限,非写入) | probe-exe-ipc-fs-v1 | 🟢 | 2026-10-06 实测:删除拒绝(winerror 5),哨兵文件完好 |

## D. 网络边界(OS 层,AppContainer capability-0)

| # | 安全点 | 来源 | 状态 | 现有证据 |
|---|---|---|---|---|
| D1 | 外部 TCP IPv4 拒绝(10013,before/after 对照) | tcp_external_v4 | 🟢 | PASS |
| D2 | 外部 TCP IPv6 拒绝 | tcp_external_v6 | 🟢 | PASS |
| D3 | 回环 TCP IPv4 拒绝或测得超时(nonce 无送达证明) | tcp_loopback_v4 | 🟢 | PASS |
| D4 | 回环 TCP IPv6 同上 | tcp_loopback_v6 | 🟢 | PASS |
| D5 | 回环 UDP IPv4 无送达(nonce 前后对照) | udp_loopback_v4 | 🟢 | PASS |
| D6 | 回环 UDP IPv6 同上 | udp_loopback_v6 | 🟢 | PASS |
| D7 | **外部 UDP IPv4** | probe-udp-external-v1 | 🟢 | 2026-10-06 实测:sendto 成功但**静默丢弃**(LAN 接收器健康对照下零命中沙箱 nonce) |
| D8 | **外部 UDP IPv6** | probe-udp-external-v1 | 🟢 | 同上(与 v4 共享出站丢弃路径,见报告局限 2) |
| D9 | **局域网主机** | probe-udp-external-v1 + probe-exe-ipc-fs-v1 | 🟢 | UDP 零送达 + TCP 拒绝(超时),监听器零命中 |
| D10 | **DNS 解析(OS 层)** | probe-udp-external-v1 | 🟢 | 容器 getaddrinfo 失败(11001),宿主对照两次 resolved |
| D11 | **非 Python 进程出网** | probe-exe-ipc-fs-v1 + probe-raw-ipc3-v1 | 🟢 | curl 超时 rc28、certutil ERROR_NOT_CONNECTED、powershell 可执行但请求 DENIED |
| D12 | **原始套接字 / ICMP** | probe-raw-ipc3-v1 | 🟢 | 可创建可发送,带 nonce echo 无应答(宿主 ping 对照 rc0)→ 静默丢弃 |
| D13 | **WinHTTP/WinINET** | probe-raw-ipc3-v1 | 🟢 | certutil(WinHTTP 栈)0x800708CA 无连接 + powershell Invoke-WebRequest DENIED |

## E. 纵深防御 shim(如实定位:非硬边界)

| # | 安全点 | 来源 | 状态 | 现有证据 |
|---|---|---|---|---|
| E1 | Python 层封堵 connect/connect_ex/sendto/getaddrinfo | net_guard.py sitecustomize | 🟢 | 代码自测 |
| E2 | 死代理环境变量(HTTP(S)/ALL_PROXY→127.0.0.1:9,NO_PROXY 空) | net_guard.py | 🟢 | 代码自测 |
| E3 | 边界如实文档化(_socket/非 Python 子进程可绕过;network_isolation 保持 UNVERIFIED) | net_guard.py docstring | 🟢 | 代码声明 |

## F. 其他 IPC / 渗透面(2026-10-06 全部实测)

| # | 安全点 | 来源 | 状态 | 现有证据 |
|---|---|---|---|---|
| F1 | **注册表写拒绝** | probe-exe-ipc-fs-v1 | 🟢 | HKLM 拒绝(5)、HKCU 拒绝(5),宿主 HKCU 零泄漏 |
| F2 | **命名管道** | probe-ipc4-v1 + probe-ipc5-v1 | 🟢 | 打开宿主管道拒绝(5)、自建管道拒绝(5),双向不通 |
| F3 | **邮件槽** | probe-raw-ipc3-v1 + probe-ipc4-v1 | 🟢 | 打开宿主邮件槽拒绝(5),宿主零接收 |
| F4 | **命名共享内存节** | probe-ipc5-v1 + probe-ipc6-v1 | 🟢 | 双向命名空间隔离:容器打不开宿主节(5)、宿主找不到容器节(2)、宿主节内容未被改写 |
| F5 | **剪贴板** | probe-ipc4-v1 | 🟢 | OpenClipboard 拒绝(5),宿主剪贴板零变化 |
| F6 | **窗口消息** | probe-raw-ipc3-v1 | 🟢 | FindWindow 找不到宿主窗口,零消息送达 |

## 缺口汇总(已全部闭合)

- 原 14 项 🔴 GAP 已于 2026-10-06 全部实测转绿(6 批探针,证据在本目录)。
- 详见 FULL_SURFACE_REPORT.md;门禁是否解禁由 Codex 独立复验后裁定,不自行放行。

## 已核实的既有证据

- 16 项联合验收 production-joint-independent-review-v2.json:16/16 PASS,production_gate=CLOSED(范围有限),certificate_written=False
- 旧 8 探针(2026-10-04):P3b 外部 UDP SENT——经本轮带接收器对照的实测澄清为"发送成功但静默丢弃",非泄漏
- isolation_acceptance.py 已退役(legacy),replacement=network_acceptance.py(仅 local loopback 范围)
- production_isolation_acceptance.py 因"Preserve previous raw evidence"拒绝覆写——新证据已走新具名路径(本目录)
