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
| C6 | **授权目录内符号链接/挂载点逃逸**(在 ROOT 内建 junction 指向外部再写入) | 无 | 🔴 GAP | 未测 |
| C7 | **外部文件删除**(DELETE 权限,非写入) | 无 | 🔴 GAP | 未测 |

## D. 网络边界(OS 层,AppContainer capability-0)

| # | 安全点 | 来源 | 状态 | 现有证据 |
|---|---|---|---|---|
| D1 | 外部 TCP IPv4 拒绝(10013,before/after 对照) | tcp_external_v4 | 🟢 | PASS |
| D2 | 外部 TCP IPv6 拒绝 | tcp_external_v6 | 🟢 | PASS |
| D3 | 回环 TCP IPv4 拒绝或测得超时(nonce 无送达证明) | tcp_loopback_v4 | 🟢 | PASS |
| D4 | 回环 TCP IPv6 同上 | tcp_loopback_v6 | 🟢 | PASS |
| D5 | 回环 UDP IPv4 无送达(nonce 前后对照) | udp_loopback_v4 | 🟢 | PASS |
| D6 | 回环 UDP IPv6 同上 | udp_loopback_v6 | 🟢 | PASS |
| D7 | **外部 UDP IPv4 拒绝** | 无(旧 P3b 显示 SENT) | 🔴 GAP | 旧 2026-10-04 探针 sendto 8.8.8.8:53 成功——必须堵住或证明送达失败 |
| D8 | **外部 UDP IPv6 拒绝** | 无 | 🔴 GAP | 未测 |
| D9 | **局域网主机拒绝**(192.168.x / 10.x / 链路本地,与互联网区分) | 无(外部只测 8.8.8.8) | 🔴 GAP | 未测 |
| D10 | **DNS 解析拒绝(OS 层)**——原生代码 getaddrinfo,不经 Python shim | 无 | 🔴 GAP | shim 层已封;OS 层未测 |
| D11 | **非 Python 进程出网**——容器内 powershell/curl/其他 exe 的原生网络 | 无(P5 只测 python 子进程句柄继承) | 🔴 GAP | 未测 |
| D12 | **原始套接字 / ICMP** | 无 | 🔴 GAP | 未测 |
| D13 | **WinHTTP/WinINET 出网**(绕过 socket shim 的 HTTP 栈) | 无 | 🟡 PARTIAL | 仅死代理环境变量(Python 客户端);原生 WinHTTP 未测 |

## E. 纵深防御 shim(如实定位:非硬边界)

| # | 安全点 | 来源 | 状态 | 现有证据 |
|---|---|---|---|---|
| E1 | Python 层封堵 connect/connect_ex/sendto/getaddrinfo | net_guard.py sitecustomize | 🟢 | 代码自测 |
| E2 | 死代理环境变量(HTTP(S)/ALL_PROXY→127.0.0.1:9,NO_PROXY 空) | net_guard.py | 🟢 | 代码自测 |
| E3 | 边界如实文档化(_socket/非 Python 子进程可绕过;network_isolation 保持 UNVERIFIED) | net_guard.py docstring | 🟢 | 代码声明 |

## F. 其他 IPC / 渗透面(当前零证据)

| # | 安全点 | 来源 | 状态 | 现有证据 |
|---|---|---|---|---|
| F1 | **注册表写拒绝**(profile hive 之外) | 无 | 🔴 GAP | 未测 |
| F2 | **命名管道**(本地,含跨用户/匿名) | 无 | 🔴 GAP | 未测 |
| F3 | **邮件槽** | 无 | 🔴 GAP | 未测 |
| F4 | **命名共享内存节对象**(CreateFileMapping) | 无 | 🔴 GAP | 未测 |
| F5 | **剪贴板** | 无 | 🔴 GAP | 未测 |
| F6 | **窗口消息/全局钩子**(对无 UI 渲染 job 价值低,但属边界) | 无 | 🔴 GAP | 未测 |

## 缺口汇总

- 🔴 GAP 共 **14 项**:C6、C7、D7、D8、D9、D10、D11、D12、D13(半)、F1、F2、F3、F4、F5(、F6 低价值)
- 计划:逐点新增原生探针(复用 native-transport 机制,新文件不覆盖旧证据),每点独立运行收集证据;全部转绿后出全表面联合验收报告,才可报解禁。

## 已核实的既有证据

- 16 项联合验收 production-joint-independent-review-v2.json:16/16 PASS,production_gate=CLOSED(范围有限),certificate_written=False
- 旧 8 探针(2026-10-04):P3b 外部 UDP SENT——佐证 D7 是真实缺口
- isolation_acceptance.py 已退役(legacy),replacement=network_acceptance.py(仅 local loopback 范围)
- production_isolation_acceptance.py 因"Preserve previous raw evidence"拒绝覆写——新证据须走新具名路径
