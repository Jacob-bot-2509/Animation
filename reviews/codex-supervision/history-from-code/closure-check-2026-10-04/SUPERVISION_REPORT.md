# 继承句柄与进程树修复：本阶段复核完成

2026-10-04，提交 `f24e97edb8bc739675ff4c511df169954adfc7f0`，重放脚本 SHA-256 `1abfcbe589b01bc9904a353af67360a12b8403fc094e5b00c01a2ad0dfaa5555`。

**本阶段两项核心修复及独立重放已收口。完整网络隔离、沙箱视频渲染尚未验收，生产门禁仍关闭。**

## 已确认

- 原先五处不存在的 `k32.get_last_error` 调用已移除，改为在清理前缓存真实错误。
- 兜底终止使用已持有并核验身份的同一 HANDLE，终止后等待确认退出；等待错误或超时不算清理成功。
- 原始返回时退出状态没有被补救清理覆盖。
- A1 普通正对照确实读取精确哨兵；沙箱令牌/API 成功、句柄读取被 OS 拒绝、退出码正确。
- A2 真实超时与正常退出场景均确认子进程退出，没有动用人工终止。
- 当前原生结果绑定的脚本、AppContainer、JobObject 三份哈希均与代码一致；四个核心/测试文件及门禁源码没有被更改。
- Claude 内置 9 项判定及故障回归记录通过；本轮在同哈希固定快照上运行的 8 项独立模拟测试全部通过。

证据：[源码绑定与门禁核验](closure-evidence.json)、[原生重放结果快照](native-result-snapshot.json)、[固定源码](source-snapshot.py)、[8 项独立模拟结果](latest-fault-results.json)、[可复用测试工具](check_error_branches.py)。

本轮独立模拟没有创建进程、profile 或修改 ACL。首次测试把等待错误的未知状态 `None` 限定为 `False` 过严，并要求未动用终止时的 `exit_confirmed=True`；已按正确语义调整：未知状态不得被判成功，已有 `alive_before_cleanup=False` 能证明进程已退出。初始结果保留在 [字段约定检查记录](first-field-convention-results.json)，没有把测试约定差异归为源代码缺陷。

核心修复之前的原生复验和全套回归见 [修复报告](../sandbox-fix-2026-10-04/FIX_REPORT.md)。本轮认可限于继承句柄与受控进程树及其复验工具，不扩展为全部隔离能力通过。

## 下一阶段监督安排

已通知 Claude 在支持目录中准备网络验收：本机 TCP、UDP、IPv6 的真实随机 nonce 收包正反对照，确认真实 AppContainer 令牌与无网络 capability，排除 Python shim。普通控制失败、IPv6 不可用、拒连、无法解释的超时均不得自动算 PASS。

依赖使用独立副本，ACL 限定自有副本/工作目录；临时 profile 使用系统 API 清理并核对目录和 HKCU 映射。禁止修改原工具链 ACL、loopback 豁免、防火墙或 C 系统文件。核心四个文件及生产门禁不在 Claude 修改范围内。

外网 TCP 和完整沙箱 MathTex/视频渲染仍需后续补证。门禁保持关闭，待全部必要隔离证据复验后再审查接入。
