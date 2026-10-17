# IPv6 双端实验 — 本地侧结论（2026-10-17）

用户待办：`下午四点半做ipv6双端实验`（id `df2964ba-fcfc-4f33-876f-7dd00d92c82b`）。
本报告覆盖**本机侧（Codex 侧）能实际测量的全部证据**，并如实给出结论与阻塞条件。
本报告不声称已完成外部 IPv6 双端实验。

## 结论

**BLOCKED_NO_IPV6_PATH — 无法成立。** 两项独立测量同时阻断：

| 维度 | 测量结果 | 判定 |
|---|---|---|
| 本机 IPv6 地址 | `Get-NetIPAddress -AddressFamily IPv6` 返回 **0 条**（无全局/ULA 地址） | 无 IPv6 栈可用 |
| IPv6 默认路由 | `Get-NetRoute -AddressFamily IPv6` 无 `::/0` | 无法出站 |
| 公网 IPv6 可达性 | `ping -6 2001:4860:4860::8888` → `transmit failed`，2/2 丢包 | 不可达 |
| 探针发射授权 | `configs/witness_automation.local.json` 的 `allow_probe_emission = false` | Codex 侧结构上不可发射 |

**测量来源说明**：上表地址/路由两行来自**本会话工具直接调用**（权威读数）。
harness 内的 payload 子进程查 WMI 时被拒（`HRESULT 0x80041003`，`拒绝访问`），
这两条读数本身不可用；但同一副本里的 `ping -6` 由子进程执行，结果同样是不可达，
与直接调用一致。因此结论不依赖被拒的 WMI 读数。

判定口径：`has_ipv6_address=false`、`public_ipv6_reachable=false`、`probe_emission_allowed=false`。
机器可读证据：[ipv6-experiment.json](ipv6-experiment.json)（含 `direct_tool_measurement` 段）。

**因此本轮没有可成立的 D2（外部 IPv6 TCP）/ D8（外部 IPv6 UDP）证据，D2/D8 继续记 GAP**，与 2026-10-13 用户授权的延期口径一致。本报告不改变 `production=CLOSED`，不改变任何隔离资格。

## 证据文件与退出码

| 产出 | 路径 | 状态 |
|---|---|---|
| 实验 harness | [run_ipv6_experiment.py](run_ipv6_experiment.py) | 本次新建 |
| 测量证据（JSON） | [ipv6-experiment.json](ipv6-experiment.json) | 已生成（本目录） |
| 原始运行阶段产物 | `archives/reviews/codex-supervision/2026-10-17-ipv6-dual-end-staging/` | 已生成（含 `unittest.*.txt`） |
| harness 退出码 | `2` | `BLOCKED_NO_IPV6_PATH`（非 PASS，也非 harness 崩溃） |

脚本内三阶段：`host_ipv6`（只读系统查询）、`emission_governance`（只读配置）、`offline_literal_tests`（离线规则测试）。

## 离线规则测试未能执行（环境限制，如实记录）

`tests/test_sandbox_external_driver.py` 共 35 项，覆盖 IPv6 外部作用域拒绝
（`test_same_host_and_same_64_cannot_be_external`）、通配/回环/多播拒绝、
receiver 必须 `ipv6_only`、10013 归因等关键规则。本次**未能跑通**：

- 原始文件把 scratch 目录硬编码在 `reviews/codex-supervision/2026-10-09-witness-input-test-work`；
- 本会话中**普通子进程对 `reviews/`、`runs/` 只读**（`PermissionError: [Errno 13]`），
  且 `archives/`、`tempfile.gettempdir()` 下的 `mkdir` 同样被拒（`WinError 5`）；
- 结果 `Ran 35 tests … FAILED (errors=58)`，全部错误发生在 `setUp` 建目录阶段，**不是规则断言失败**。

已采用最小改动：复制测试到 staging，仅把 `ROOT` 钉到项目根、scratch 重定向到临时目录；
未修改 `tests/` 下任何原件。此项作为**未完成**列在“下一步”，不记为通过。

## Codex 的职责边界（为什么不在本机发射探针）

依据 `reviews/codex-supervision/2026-10-08-auto-mail/TASK.md` 与
`archives/reviews/codex-supervision/2026-10-13-witness-automation-design/DESIGN.md`：

- 探针发射、接收器启动、双端实验排期由**用户在会话中直接授权后 Claude 执行**；
- Codex 负责第二三层（材料打包、验哈希、v3 预检、受限注册对账）与独立审查，
  工具链**没有探针发射入口**；
- 活动配置 `allow_probe_emission=false` 是这条边界的机器可读体现。

所以即使本机有 IPv6，Codex 也不会自行发射；本报告是**能力测量**，不是实验执行。

## 解除阻塞需要什么

1. **一台有可达公网 IPv6 的证人机**（具体 IPv6 字面地址，不能是回环/通配/多播，
   且不能与本机同 /64）。本机当前无任何 IPv6 地址，说明两端都还没就绪。
2. **由你授权 Claude 在另一端启动 v3 接收器**（`witness_receiver_v3.exe`，SHA
   `02d781bc…e2eb44bf` 已在配置中钉住），并在本机侧批准一次探针发射；或明确把
   发射任务交给 Claude，Codex 只做收尾对账。
3. 若希望本机作为发送端，还需先给本机接入 IPv6（当前网卡没有 IPv6 地址，
   `ms_tcpip6` 绑定状态也读不到）。

## 复现命令

```powershell
cd D:\Animation-Model-Training
& "D:\Python Interpreter 3147\python.exe" -X utf8 -B `
  reviews/codex-supervision/2026-10-17-ipv6-dual-end/run_ipv6_experiment.py `
  --out D:\Animation-Model-Training\archives\reviews\codex-supervision\2026-10-17-ipv6-dual-end-staging
# 预期：exit 2，verdict=BLOCKED_NO_IPV6_PATH
```

只读复核（不需要 harness）：

```powershell
Get-NetIPAddress -AddressFamily IPv6            # 预期：无输出
Get-NetRoute -AddressFamily IPv6 -ErrorAction SilentlyContinue | Where-Object DestinationPrefix -eq '::/0'   # 预期：无输出
ping -6 -n 2 2001:4860:4860::8888               # 预期：transmit failed
```

## 时间说明

待办标注“下午四点半”，board 的 `schedule` 为 `2026-10-17T16:00`，但 `dispatchedAt`
已被置为 `1792210546191`（本次派发），实际执行时间约 **12:15**。若 16:30 才是你预期的
窗口，本条结论在 16:30 仍成立（若届时网络接入 IPv6，重跑复现命令即可）。

## 未建立 / 未改变

- 未建立：外部 IPv6 双端运行、沙箱 IPv6 探针投递、D2/D8 任何通过性证据。
- 未改变：`production=CLOSED`、D1/D7 依赖条件、全局隔离 `NOT_ESTABLISHED`。
- 未发射任何探针、未启动接收器、未修改 `configs/`、`tests/`、`data/`。
