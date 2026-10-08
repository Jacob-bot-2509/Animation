# 沙箱安全点与证据清单（待独立验收）

原枚举为43点，不能按“16既有+14缺口+10结构”算成40点。旧16个检查仅有具名范围的历史结论；各点原生覆盖及清单穷尽性未获全表面认证。当前30项GREEN仅指注册夹具矩阵，全43点尚未验收。生产门禁CLOSED；候选未准入，未开始训练。

状态：GREEN覆盖当前SHA绑定的注册夹具矩阵，非穷尽性承诺；PARTIAL为矩阵未齐；GAP为缺少当前完整对应证明。来源类别必须逐项记录，不能以代码强制代替原生测试。

| 点 | 安全点 | 原记录来源 | 当前状态 | 证据说明 |
|---|---|---|---|---|
| A1 | 每次 job 全新 UUID profile,不可复用 | private_profile.py `_profile_grants` | GREEN | 当前具名原生源码/完整输出/父token-profile-ACL与15项实现SHA核对 |
| A2 | SID 有效且容器 token SID 与 profile SID 一致 | isolation_evidence.py `_parent` | GREEN | 当前具名原生源码/完整输出/父token-profile-ACL与15项实现SHA核对 |
| A3 | 容器 token is_appcontainer=True | 同上 | GREEN | 当前具名原生源码/完整输出/父token-profile-ACL与15项实现SHA核对 |
| A4 | capability_count == 0(无任何能力) | 同上 | GREEN | 当前具名原生源码/完整输出/父token-profile-ACL与15项实现SHA核对 |
| A5 | profile 专属存储目录 job 后删除 | 同上 | GREEN | 当前具名原生源码/完整输出/父token-profile-ACL与15项实现SHA核对 |
| A6 | 临时 ACL 授权仅限 精确四根（venv、MiKTeX、D:\Python、具名work）,拒绝符号链接/重解析点根 | private_profile.py `_profile_grants` | GREEN | 真实root/ancestor junction被授权前拒绝；CreateProfile=0，DACL不变 |
| A7 | ACL 授权 job 后回收(before==after,SHA 绑定) | 同上 | GREEN | 当前具名原生源码/完整输出/父token-profile-ACL与15项实现SHA核对 |
| A8 | 授权前根目录不存在该新 SID 的既有 ACE | 同上(`Fresh UUID SID already granted` 检查) | GREEN | 真实新SID既有ACE冲突被拒；grant=0，profile删除且DACL恢复 |
| A9 | ACL 编辑跨进程串行化(transport.lock) | isolated_profile | GREEN | 两宿主进程争同一lock；第二个errno13且CreateProfile=0，首个清理 |
| B1 | 仅继承 stdio 句柄(挂起创建→分配 Job→恢复) | appcontainer.py run_appcontainer | GREEN | 真实可继承宿主文件句柄未入容器，stdio白名单3 |
| B2 | 根进程退出 → 整树停止 | 同上 | GREEN | 根退出后持有同一child/grandchild HANDLE等待均为0 |
| B3 | 超时 → 整树终止(含孙进程) | 同上 | GREEN | 原生超时后持有同一child/grandchild HANDLE等待均为0 |
| B4 | 内存上限 2 GiB(64MiB 块,超限 rc17 拒绝) | isolation_evidence.judge memory_limit | GREEN | 2 GiB job限额，64 MiB块，实际rc17 |
| B5 | Job 分配失败不恢复子进程(fail-closed) | 生命周期单元测试 | GREEN | 真实挂起进程Job分配故障；Resume=0，进程终止，profile清理 |
| C1 | 项目外读拒绝 | 16 项 file_read_outside | GREEN | 存活自有夹具前后健康对照；原生Win5拒绝且宿主未变 |
| C2 | 项目外写拒绝(含 marker 缺失复核) | file_write_outside | GREEN | 存活自有夹具前后健康对照；原生Win5拒绝且宿主未变 |
| C3 | D:\Python 工具链写拒绝 | file_write_runtime | GREEN | 存活自有夹具前后健康对照；原生Win5拒绝且宿主未变 |
| C4 | 跨 run 持久写拒绝 | cross_run_write / cross_run_cache_write | GREEN | 存活自有夹具前后健康对照；原生Win5拒绝且宿主未变 |
| C5 | job 期间私有/受保护文件不变(before/after SHA) | 同上 | GREEN | 15个具名受保护实现/runtime字节前后相同 |
| C6 | **授权目录内符号链接/挂载点逃逸**(在 ROOT 内建 junction 指向外部再写入) | 无 | GREEN | work内预建junction已验证；Win5拒写，自有外部目标DACL不变 |
| C7 | **外部文件删除**(DELETE 权限,非写入) | 无 | GREEN | 存活自有夹具前后健康对照；原生Win5拒绝且宿主未变 |
| D1 | 外部 TCP IPv4 拒绝(10013,before/after 对照) | tcp_external_v4 | GAP | 缺当前受控接收端/协议健康对照或完整采集，保留GAP |
| D2 | 外部 TCP IPv6 拒绝 | tcp_external_v6 | GAP | 缺当前受控接收端/协议健康对照或完整采集，保留GAP |
| D3 | 回环 TCP IPv4 拒绝或测得超时(nonce 无送达证明) | tcp_loopback_v4 | GREEN | 同端点协议nonce前后健康对照；沙箱nonce未送达；尝试后观察≥20 s |
| D4 | 回环 TCP IPv6 同上 | tcp_loopback_v6 | GREEN | 同端点协议nonce前后健康对照；沙箱nonce未送达；尝试后观察≥20 s |
| D5 | 回环 UDP IPv4 无送达(nonce 前后对照) | udp_loopback_v4 | GREEN | 同端点协议nonce前后健康对照；沙箱nonce未送达；尝试后观察≥20 s |
| D6 | 回环 UDP IPv6 同上 | udp_loopback_v6 | GREEN | 同端点协议nonce前后健康对照；沙箱nonce未送达；尝试后观察≥20 s |
| D7 | **外部 UDP IPv4 拒绝** | 无(旧 P3b 显示 SENT) | GAP | 缺当前受控接收端/协议健康对照或完整采集，保留GAP |
| D8 | **外部 UDP IPv6 拒绝** | 无 | GAP | 缺当前受控接收端/协议健康对照或完整采集，保留GAP |
| D9 | **局域网主机拒绝**(192.168.x / 10.x / 链路本地,与互联网区分) | 无(外部只测 8.8.8.8) | GAP | 缺当前受控接收端/协议健康对照或完整采集，保留GAP |
| D10 | **DNS 解析拒绝(OS 层)**——原生代码 getaddrinfo,不经 Python shim | 无 | GAP | 缺当前受控接收端/协议健康对照或完整采集，保留GAP |
| D11 | **非 Python 进程出网**——容器内 powershell/curl/其他 exe 的原生网络 | 无(P5 只测 python 子进程句柄继承) | GAP | 缺当前受控接收端/协议健康对照或完整采集，保留GAP |
| D12 | **原始套接字 / ICMP** | 无 | GAP | 缺当前受控接收端/协议健康对照或完整采集，保留GAP |
| D13 | **WinHTTP/WinINET 出网**(绕过 socket shim 的 HTTP 栈) | 无 | GAP | 缺当前受控接收端/协议健康对照或完整采集，保留GAP |
| E1 | Python 层封堵 connect/connect_ex/sendto/getaddrinfo | net_guard.py sitecustomize | GREEN | 当前bootstrap四种Python拦截调用实测阻断 |
| E2 | 死代理环境变量(HTTP(S)/ALL_PROXY→127.0.0.1:9,NO_PROXY 空) | net_guard.py | GREEN | 当前原生环境八项代理变量逐值核对 |
| E3 | 边界如实文档化(_socket/非 Python 子进程可绕过;network_isolation 保持 UNVERIFIED) | net_guard.py docstring | GREEN | 当前源码边界声明；此项是文档验证，非原生网络实验 |
| F1 | **注册表写拒绝**(profile hive 之外) | 无 | GREEN | 存活自有夹具前后健康对照；原生Win5拒绝且宿主未变 |
| F2 | **命名管道**(本地,含跨用户/匿名) | 无 | PARTIAL | 命名本地管道Win5；匿名两端继承补测通过；仍缺跨用户健康夹具 |
| F3 | **邮件槽** | 无 | GREEN | 存活自有夹具前后健康对照；原生Win5拒绝且宿主未变 |
| F4 | **命名共享内存节对象**(CreateFileMapping) | 无 | PARTIAL | Local mapping Win5；Global宿主创建Win5，无SeCreateGlobalPrivilege健康夹具 |
| F5 | **剪贴板** | 无 | GAP | 独立window station三种掩码均Win5；剪贴板API调用0，未验收 |
| F6 | **窗口消息/全局钩子**(对无 UI 渲染 job 价值低,但属边界) | 无 | GAP | 缺隔离会话的窗口消息/全局hook各自健康对照，未验收 |

当前计数：43点=30 GREEN+2 PARTIAL+11 GAP，FAIL=0。A8/A9/B5已有真实宿主Windows生命周期/故障夹具，E1/E2已有当前原生容器实测；E3仍为文档声明验证，必须与原生分列。旧16项历史检查结果保留，不能扩展为43点通过。

## 本次探索结果的关键限制

- D7/D8：sendto返回不是外部投递；缺外部IPv4/IPv6受控接收器，二者不能借用本机NIC、DNS、TCP或“共享路径”来证明。
- D9：28.0.0.1是本机所选接口；另一台LAN主机未受控验证。
- D10：11001与固定example.com不是明确权限拒绝，也没有可靠的DNS出站采集/缓存分离。
- D11/D13：curl超时、缺失PowerShell、certutil失败不能扩大为所有非Python/WinHTTP/WinINET出网拒绝。须精确nonce与实际协议健康对照。
- D12：原始socket可创建/可send而无回显，不能直接声称静默丢弃；应验证echo类型、ID、序号、完整nonce及双向健康通路。
- C6：junction创建失败没有测试预先存在的链接逃逸；链接未存在时的ENOENT不是权限拒绝。
- F4：释放对象后查不到不能证明隔离；双侧应在对象存活期间测试，并正确绑定64位HANDLE及API错误。
- F5：不得清空、读取或记录用户剪贴板；须隔离测试会话。旧探针已改写用户剪贴板为测试nonce且未保留原内容，不能补造恢复记录。
- F6：HostWindow线程/类型/ABI失败，或FindWindow找不到，都不能作为窗口消息/钩子隔离通过。

## 修正运行器

六支旧脚本转到v2共同契约，默认打印计划；`--execute-native`才运行具名自有夹具。完整保留原始传输、源码/实现绑定、token/profile/ACL证据和接收器生命周期，精确nonce归因，UNKNOWN不能GREEN。F5/F6保持未验证，不访问用户桌面数据。不覆盖v1原始回执、不写生产证书；后续新证据仍需独立复验。

记账脚本只读分析并另存，禁止根据总次数硬编码沙箱零命中。raw3原始字节已按watcher首次SHA精确恢复，覆写版本另存。所有探索材料仍未获生产验收。

## 2026-10-06 本机修复检查点

用户安排“暂无资源，先完成本机部分”。当前主回执与匿名补测字节保持；C6/C7/F1/F3等旧限制对应的本机夹具已在本轮补齐。上方“本次探索结果”是旧v1限制，历史JSON保留。当前结论及13项剩余资源见 [Codex本机修复报告](../codex-supervision/2026-10-06-all43-sandbox-repair/FIX_REPORT.md)。生产CLOSED，无全43证书。
