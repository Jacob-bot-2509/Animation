# 沙箱全安全点联合验收报告(exec_isolation 门禁 ③)

- 日期:2026-10-06(UTC+8 晚)
- 依据:用户裁决——**只有沙箱所有安全点检测为绿才解禁**;16 项有限范围测试不足以放行。
- 方法:每个缺口安全点新增原生探针,走生产同款启动路径(`run_code(mode='probe')`:
  全新 UUID AppContainer profile、同 grants、同 token/JobObject/防火墙机制),宿主机 before/after
  健康对照证明测试通路本身可用。全部证据 JSON 在本目录,绝不覆盖旧证据。
- 结论:**全部安全点测得为绿(共 40 点;既有 16 项 + 本轮 14 缺口 + 结构 10 项)。
  门禁是否解禁由 Codex 独立复验后裁定,本报告不自行放行。**

## 一、本轮 14 项缺口结果(6 批探针)

| # | 安全点 | 探针 | 结果 | 关键证据 |
|---|---|---|---|---|
| D7/D8 | 外部 UDP v4/v6 | batch1 | 🟢 | sendto 成功但**静默丢弃**:LAN 接收器(before/after 健康对照)零命中沙箱 nonce |
| D9 | 局域网 UDP | batch1 | 🟢 | 同上,直接证明无送达 |
| D10 | OS 层 DNS | batch1 | 🟢 | 容器 getaddrinfo 失败(11001),宿主对照两次 resolved |
| D11 | 非 Python 程序出网 | batch2/3 | 🟢 | curl.exe 超时 rc28;certutil 0x800708CA(ERROR_NOT_CONNECTED);powershell 全路径可执行但 Invoke-WebRequest DENIED;监听器零命中 |
| D12 | 原始套接字/ICMP | batch2/3 | 🟢 | 可创建、可发送,但带 nonce 的 echo 请求**无应答**(宿主 ping 对照 rc0 正常)→ 静默丢弃 |
| D13 | WinHTTP/WinINET | batch3 | 🟢 | certutil(WinHTTP 栈)ERROR_NOT_CONNECTED + powershell DENIED |
| F1 | 注册表写 | batch2 | 🟢 | HKLM 拒绝(5)、HKCU 拒绝(5),宿主 HKCU 零泄漏 |
| F2 | 命名管道 | batch4/5 | 🟢 | 打开宿主管道拒绝(5)、自建管道拒绝(5)——双向不通 |
| F3 | 邮件槽 | batch3/4 | 🟢 | 打开宿主邮件槽拒绝(5),宿主零接收 |
| F4 | 命名共享内存节 | batch5/6 | 🟢 | 双向命名空间隔离:容器打不开宿主节(5),宿主找不到容器节(2),宿主节内容未被改写;容器建的 Global 节仅存在于其私有命名空间 |
| F5 | 剪贴板 | batch4 | 🟢 | OpenClipboard 拒绝(5),宿主剪贴板内容零变化 |
| F6 | 窗口消息 | batch3 | 🟢 | FindWindow 找不到宿主窗口(隔离),零消息送达 |
| C6 | 符号链接/挂载点逃逸 | batch2 | 🟢 | junction **创建即被拒**(拒绝访问),写通道无从建立 |
| C7 | 外部文件删除 | batch2 | 🟢 | 删除宿主机文件拒绝(5),哨兵文件完好 |
| 附加 | 局域网 TCP | batch2 | 🟢 | 连接拒绝(超时),监听器零命中 |

## 二、既有证据复核(16 项 + 结构)

- 16 项联合验收(production-joint-independent-review-v2.json):16/16 PASS,已独立重算。
- profile/ACL/JobObject 结构 10 项(A1-A9、B1-B5 与既有 16 项重叠部分)沿用既有证据,
  本轮每批探针运行同样触发 fresh profile 全生命周期,parent_evidence 均正常。

## 三、如实局限(不夸大)

1. 外部 IP(8.8.8.8 等)的 UDP/ICMP 送达无法从本机直接观测(无外部接收器);
   证据链 = 同一出站路径的局域网接收器零命中 + DNS 解析失败 + TCP 拒绝(10013/超时)
   + WinHTTP ERROR_NOT_CONNECTED,共同指向防火墙静默丢弃/拒绝。
   如需完全闭合外部可达性,需要一个外部 vantage point(另一台机器的接收器)。
2. IPv6 外部无 v6 接收器对照,与 v4 共享同一丢弃路径推断。
3. 批次四 ipc4 一次 section_inbound 读数("opened":true)与批次六决定性数据矛盾,
   已定位为该次 GetLastError 陈旧值伪影;以批次六(所有返回值逐项记录)为准。
4. 批次二/三的管道/邮件槽早期读数受 ctypes 64 位句柄截断 bug 污染,污染证据已
   具名保全(probe-ipc4-v1-contaminated-truncation.json),修正后重测结论以批次四/五为准。

## 四、证据文件清单

- probe-udp-external-v1-results.json(D7/D8/D9/D10)
- probe-exe-ipc-fs-v1-results.json(D11/F1/C6/C7/D12 创建/局域网 TCP)
- probe-raw-ipc3-v1-results.json(D12 实测/F6/D13/F4 反向)+ fix_ipc3_accounting.py 修正记录
- probe-ipc4-v1-results.json(F2/F3/F5 错误码)+ probe-ipc4-v1-contaminated-truncation.json(污染保全)
- probe-ipc5-v1-results.json(F2 双向/F4 双向)
- probe-ipc6-v1-results.json(F4 决定性/会话+Global 命名空间)
- SAFETY_POINT_ENUMERATION.md(权威 40 点清单,状态全部更新为绿)

## 五、待办

- Codex 独立复验本报告与全部证据
- 全绿 + 独立复验通过后,才可讨论解禁;解禁仍须用户授权
