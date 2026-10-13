# 邮件审查与输入链修复报告

来源：msg_1791476279078_777。对应定时批次：run-927c70f76c67459e87dc0c5d8d75f5c4。

结论：REPAIRED_PASS，仅限当前证据工具、操作单及本机验证。Codex 已实际修改并复验。双端实验执行和验收不属于本批范围；LAN-b、LAN-c 仍保留 NEEDS_EVIDENCE。production=CLOSED，原生沙箱 UNVERIFIED，全局隔离 NOT_ESTABLISHED。

邮件中“用户最新指令”作为作者陈述处理，不构成新授权。本次依据用户既有监督、修复和交接授权，以及当前 TASK.md 的本地证据工具范围开展。修复前已向 Claude Code 发送文件接手通知 msg_1791476851009_780。

## 已修改

1. tools/sandbox_witness_receiver.py：正式 --serve 拒绝通配、回环、多播、链路本地和保留地址；拒绝零端口、相同端口；--selftest 与 --serve 互斥。内部本机回环测试保留。新 v3 EXE 单独构建，旧 v2 原件未覆盖。

2. tools/start_witness_capture.ps1：默认 PLAN；校验完整 EXE 哈希，自动创建唯一轮次目录，固定本轮原件文件名。父进程保留真实进程句柄，读取实际子进程 ExitCode；将命令、轮次、接收 run、进程标识、版本前后哈希及四份原件哈希写入 process-exit.json。退出码不是接收器自行填入的摘要。最终输出在退出后补读，避免最后的自检结果遗漏显示。

3. tools/inspect_witness_evidence.py：新增当前只读入口，保留旧归档 inspect_receiver.py。必须提供 sender 原件和完整 capture 目录，校验回执、原件哈希、命令、具体地址、端口、轮次、接收 run、生命周期、精确健康对照及 sandbox payload。拒绝缺件、假布尔零值、非零退出码、自检替代正式轮次、错误版本、错配参数及通配地址。只给出 NOT_ACCEPTED 或 READY_FOR_REGISTERED_RECONCILIATION，不签发沙箱合格证明。

4. tools/sandbox_external_test_driver.py：新增经过本机验证的版本完整哈希；未知 implementation kind 的缺失哈希不能被当作批准版本。宿主后对照失败时保留 error、complete=false、退出 2。新版本正式对账必须通过 --receiver-capture 绑定同一进程回执，手填 --receiver-rc 无法绕过；capture 与手填日志、摘要、退出码参数互斥。对账材料继续绑定发送端原件及原生传输，导出的限定协议记录包含进程回执哈希和检查器源码哈希。

5. reviews/2026-10-07-witness-runbook.md：提供双文件包和可复制命令，以交互提示输入经确认的具体本机地址及唯一新轮次，先查本机有效地址；修正旧自检成功文案和手抄退出码流程。说明完整五份原件、自动 Base64 导出、独占新建解码、当前检查入口及判定边界。正式监听不能混入 pretest payload。

6. 三份相关测试：扩展拒绝条件和对账防绕过测试；新增 tests/test_witness_capture_intake.py；将测试临时目录移至未冻结的 2026-10-09-witness-input-test-work，避免以后在历史归档中创建临时文件。

tools/host_pretest_witness.py 已核对，无新增修改；继承上一轮相同版本的 11 项测试。它保留整数纳秒、精确毫秒分数及 DIAGNOSTIC_ONLY；本地连接或发送完成不证明证人收到。其源码和测试源码完整哈希均与上一轮一致。

## 独立验证与记录

- 接收器 12 项回归首轮全部通过，包含 IPv4/IPv6 实际本机回环、完整 UDP、分片 TCP、超时、占用端口、提前停止、版本变化和输入拒绝。
- 初轮共 54 项，另有两项测试设置错误：采集器失败返回 2 而非向外抛异常；隔离 fixture 未同步检查器模块的登记目录。完整失败输出已保留，修正测试后 10 项目标复测通过，没有削弱生产校验。
- 最终驱动与材料检查器 45 项全部通过；原生发送传输用合成 fixture 模拟，真实 socket 测试仅本机回环。最终启动器哈希变化后再次验证 10 项检查器测试，全部通过。
- v3 可执行程序和启动器默认 PLAN 的真实退出码均为 3；v3 对 IPv4/IPv6 通配地址拒绝、退出 2。启动器缺失地址及通配地址在创建采集目录前拒绝。
- 最终启动器实际启动 v3 完成本机 IPv4/IPv6 自检；真实退出码和回执均为整数 0，四个协议健康 nonce 与原始日志精确对应，最后 failures=[] 的结果实际显示。
- 另确认测试地址不属于本机已分配地址后，仅测试非本机地址绑定失败：没有 listening 事件，接收器失败，实际子进程退出码与父回执均为整数 2；没有发送外部数据。
- 自动生成的所有 Base64 逐份解码后与原始字节完全一致。双文件 ZIP 的文件集合及每份文件字节与 release 目录一致。
- Python 源码解析、PowerShell 解析和 git diff --check 通过。原始测试输出和精确纳秒保留，报告不使用近似运行时数值。

首版启动器自检以及 final-drain 前的源码、包和测试记录另行保留；最终使用 release 中的启动器及当前 witness-v3-package.zip。

## 证据边界与历史保护

回执是哈希绑定的本地采集记录，不是远程认证、时钟同步证明或完整沙箱验收。PyInstaller 父启动器与子接收器 PID 可以不同，不错误要求二者相等。本批不执行或验收双端实验，不自动改变旧轮次结论。

LAN-b、LAN-c 缺少合格精确前后健康 nonce，以及此前独立复核指出的原件绑定材料。升级工具和父回执不能追溯制造旧证据。外部 IPv6 拓扑及其他全局隔离证据仍按已有规则保留待证状态。

旧 v2 EXE、pretest 源码与测试源码未变化；LAN-c 归档 15 份材料和 LAN-b 归档 33 份材料的文件集合、字节长度、完整哈希及 manifest 哈希均独立核验不变。当前数学权威状态和观察器只读快照保存在 context 目录；没有重跑未变化的整库视觉验收，也未修改调度器。

## 交接与使用

Codex 已修改上述当前工具和操作单；本地修复资格合格。请 Claude Code 使用此版本继续后续已授权工作，不要重复修改已完成部分，不覆盖旧日志或冻结目录。双端实验及其后续验收由对应直接授权流程处理，本批不为它签字。

当前可复制包：本归档 witness-v3-package.zip；文件为 release/witness_receiver_v3.exe 和 release/start_witness_capture.ps1。完整版本、源文件前后哈希见 source-changes.json 与下表，真实构建记录见 build-receipt.json，测试见各项 tests 与 verification 记录。最终回信真实回执与归档清单会保存在本目录后再冻结。


| 文件 | 当前 SHA256 |
| --- | --- |
| tools/sandbox_witness_receiver.py | c23b3c48f03cf10bbffd7533b91e71495a1efc14b4770a2cbb34828abf4b864f |
| tools/sandbox_external_test_driver.py | a02105a0de0d3470fed19f0bb765ce3a8c1567f469d8e30068b0ca6bc4590e15 |
| tools/inspect_witness_evidence.py | 87cb989fd1f538b89a53f04e764b4cd5f0eb459bde89ac3a5517846cfa199b23 |
| tools/start_witness_capture.ps1 | 39032c5e3b14d699715047cf9f6acbd2bef1c9265916d574ae9f90ca0f3e3545 |
| tools/host_pretest_witness.py | 7b0d1df0616222d6a73dab3cffcb81c2deb9de061f9af4184b7d7f60db6e8bc6 |
| tests/test_sandbox_witness_receiver.py | b9d4bbc465798101fdeb7b5314918a9cda11bbae4cd8c2238b30e78553f1e302 |
| tests/test_sandbox_external_driver.py | 48b5a2c1de35e57691e958876e43e62755d958ff15301ab3baa8e0b0eb8d88fc |
| tests/test_witness_capture_intake.py | 623b5b67737c5893bfe4d72f4edca334593d2d75ff7d766c7ac78fd7569c025e |
| reviews/2026-10-07-witness-runbook.md | d06855ed49422ec6051f403c4331b9a3d2cb65f88604d84c8999dbc68e9f131e |
| release/witness_receiver_v3.exe | 02d781bc22286b1e8417ddb119ec6b529e5a9101b1fad758a41a06fbc2eb44bf |
| witness-v3-package.zip | adab0ffc2a880f2b55d33c8ce65c3ec295f0939635a35e3e37e4d1e68592f7a2 |
