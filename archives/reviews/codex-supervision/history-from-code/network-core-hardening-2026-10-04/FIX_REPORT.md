# 第二轮邮件复核：网络证据加固

2026-10-04。处理 Claude 的 `msg_320`、`msg_321`、`msg_322`。他独立确认上一轮 7 项修复、382/382 测试与原生证据一致，再提出 6 项加固建议并询问后续分工。我通过 `msg_323` 确认接手本轮修复及后续准备范围。

**本轮完整回归 392/392，网络回归 53/53，失败、错误和跳过均为零。修订版本的四项原生回环复验通过；结论仍仅为 `PASS_LOCAL_LOOPBACK`。外网未验收，生产门禁 CLOSED。代码已落地，尚未提交。**

## 独立复现与修复

| 邮件建议 | 独立核实及最终处理 |
|---|---|
| 1. 前对照包没有沙箱开始时间上界 | 已复现：前对照客户端结束于 2、沙箱开始于 3、前对照包到达于 25，旧判定仍通过。现在要求前控制包不晚于沙箱开始，后控制包不早于沙箱完成，并保持接收器生命周期和各客户端约束。允许前包时间等于沙箱开始的边界。 |
| 2. hex 比较可能降级 FAIL | 使用包含 hex 字母的合成 nonce 独立复现大写及零字节包裹两种形态从 FAIL 降为 UNVERIFIED。现在先解码实际字节；大小写、hex 空白和额外包头/尾字节不会掩盖完整沙箱 nonce 已送达。其它无效 hex 仍为 UNVERIFIED，普通控制必须精确整包匹配。 |
| 3. 负时间与零时长 | 已复现负监听起点和零时长沙箱尝试误通过。现在所有时间非负且有限，每个客户端 `started < finished`；补入三类客户端及整体负时间平移负例。 |
| 4. 等价 SID 编码 | 邮件所举小写豁免 SID 在现有前置格式守卫下已为 UNVERIFIED，并非新的误通过。独立发现数字前导零的等价 SID 则会误通过；只读调用 Windows SID 转换 API 确认大小写及数字前导零均转为同一 canonical SID。现在以有边界的十进制 SID 数值成分比较豁免、令牌和预期 SID；保留原始文本，非法/越界/不支持编码为 UNVERIFIED。 |
| 5. 退出码文档 | 工具 docstring 和 `--help` 的描述明确 0=有证据的本机通过、1=有证据的 FAIL、2=UNVERIFIED，包含证据无法写入的情况；写入失败原因输出 stderr。退出码不能代替 JSON 状态及范围检查。 |
| 6. close 异常丢失快照 | 用备份旧工具和新工具分别故障注入。旧工具在 `close()` 失败后丢弃已收到的沙箱 nonce，结果 UNVERIFIED；新工具保留收包、关闭时间和原接收错误，结果 FAIL，`server_complete=False`。快照本身失败也不跳过其余状态采集。这是实际异常路径的证据保存修复，并不限于畸形记录。 |

7 个输入变异的初始结果见 [初始复现](initial-reproductions.json)，该文件同时保存了真实 Windows SID 转换观测；修复结果见 [修复后复现](fixed-reproductions.json)。关闭失败的旧版/新版完整记录见 [独立故障对比](close-failure-reproductions.json)。

新增 10 个测试方法及多组子案例，覆盖时间括弧、负时间、零时长、等价/非法 SID、hex 编码及额外字节、关闭失败仍保留 FAIL、快照采集失败不丢其它状态。见 [完整测试计数](unittest-full.json)、[完整日志](unittest-full.log) 和 [网络测试计数](unittest-network.json)。

## 代码及原生复验

本轮只修改本人负责的四份文件，替换前检查 SHA、保留 [源码备份](backup/network_isolation.py) 和其余同目录备份：

- [network_isolation.py](/D:/Animation-Model-Training/src/animtrain/network_isolation.py)
- [network_acceptance.py](/D:/Animation-Model-Training/tools/network_acceptance.py)
- [test_network_isolation.py](/D:/Animation-Model-Training/tests/test_network_isolation.py)
- [test_network_acceptance.py](/D:/Animation-Model-Training/tests/test_network_acceptance.py)

当前四文件与 [安装哈希](installed-file-hashes.json) 一致。原生证据内模块和工具哈希也匹配当前源码；每项原始记录另由我独立重新判定、检查前后收包时间括弧。

| 实际场景 | 普通前后对照 | 沙箱 nonce | 沙箱结果 | 结论 |
|---|---|---|---|---|
| TCP 127.0.0.1 | 同端口 2 条，时间括弧成立 | 0 条 | net_timeout | PASS_LOCAL_LOOPBACK |
| UDP 127.0.0.1 | 同上 | 0 条 | sent_ok，未投递 | PASS_LOCAL_LOOPBACK |
| TCP ::1 | 同上 | 0 条 | net_timeout | PASS_LOCAL_LOOPBACK |
| UDP ::1 | 同上 | 0 条 | sent_ok，未投递 | PASS_LOCAL_LOOPBACK |

四项前后系统豁免查询成功、清单为空；沙箱真实 SID 匹配、能力为 0；接收线程正常结束且无错误；运行时关键文件及 `._pth` 未变，沙箱完成后的观察窗口至少 20 秒。

新证据：[loopback-73a3d431a3ed4829ab91e819c51d7027.json](native/loopback-73a3d431a3ed4829ab91e819c51d7027.json)，SHA256 `d2e3e0e1bd0b4dc97cb2b94677acf03892d30ca1f923e04639e0ef80cdab1a58`，schema 2、state COMPLETE、退出码 0。见 [运行日志](native-run.log) 和 [独立收口核验](closure-evidence.json)。契约仍为 `local-loopback-os-policy-v1`，本轮加强同一契约的证据一致性与失败信息保存。

已验收的 AppContainer、JobObject、两份生命周期回归、render_gate、停用历史入口和 Claude 支持脚本共 7 份文件的哈希保持一致，见 [保护文件检查](unchanged-files.json)。上一轮原生 JSON 的 SHA256 仍为 `d2f681f0b03ff7069386ad55323fdd68d262eaaccb281470e6a21f21cd4e7680`；原证据未改写。

## 范围及后续分工

通过仅覆盖实测本机四个端点及时间窗口；不代表外网、其它目标或完整沙箱渲染已经验收。生产门禁保持关闭。没有新增 ACL、profile、回环豁免、防火墙或审核策略修改。

已向 Claude 明确：文件读写验收继续由他准备具名工作区、合成数据和正反对照的支持脚本，再由我复核接线及原生结果；MiKTeX 先做只读依赖、空间和 D 盘副本方案，不先复制、授权或渲染；外网 TCP 要另行确定可控测试端点与受限验收计划，不因回环通过自动放行。

本轮修复与验证完成后通过 AI Bridge 回信，交还只读复核。上一轮复核报告见 [network-core-review-fix/FIX_REPORT.md](../network-core-review-fix-2026-10-04/FIX_REPORT.md)。
