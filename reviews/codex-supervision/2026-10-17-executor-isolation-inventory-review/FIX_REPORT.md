# 执行器合同与原生隔离清单：修复及独立复算

本批 run-a682d2108583407cb93bfb37a304e7d4 的两条邮件及 message_hashes 已与原始 packet 一致核验。邮件是待审材料，不作为新增授权。已先回信 Claude 明确接管两份文件，修复前逐字节留存，写回前检查没有并发修改。

| 邮件 | 本轮裁决 | 明确合格范围 |
|---|---|---|
| msg_1792209889506_863 | REPAIRED_PASS | 执行器/判定器合同 v2 的设计审查；未实现、未接线、未运行 |
| msg_1792210111536_864 | NEEDS_EVIDENCE | 清单与只读复算已修复并合格；当前原生联合验收仍有实际缺口，不签证书 |

Codex 已修改：
- reviews/data-prep/2026-10-17-submission/eval-wiring/real-executor-judge-contract.md：SHA-256 22f3492996583b643a19fb8bdc204fc44473673d5d2a152f467ac42af1eb6a7e。
- reviews/data-prep/2026-10-17-submission/exec-isolation/exec-isolation-bounded-inventory-v1.json：文件名保留原入口，内部 schema 升为 v2；SHA-256 ef8050cdc76dc0bfdc03ea2c5ca71419b1e4662dc056c0d5d9747c2dc645e066。

## 合同修复

父进程证据“文件存在且 SHA 一致”只证明字节一致，不能证明来源。v2 要求父进程独占且子进程不能改写的证据根、真实运行登记与 nonce/identity、令牌/Job/ACL/清理的实测归属，整树停止和写入者关闭后才固定最终清单。请求自报脚本路径或源码 SHA 不能批准执行。生成代码即便出自白名单模板，也必须遵守实际隔离门禁；静态实现及 Mock 可提前。

增加运行期有界输出与资源限制、严格身份/版本/输入绑定、根外与重解析点拒绝、真实格式与完整媒体解码；MP4 不能用首帧或预览冒充完整输出。画面忠实须覆盖全部必需场景和相关区间，不以抽几帧证明整段动画。

数学断言基准必须来自独立核验并冻结的正确题文与动画对象关联，不能由生成物自选恒真式。首版受限 DSL 使用整数/精确分数和白名单有限 AST，定义域、零分母、整数幂与资源上限明确；不支持根式/π等时保留原符号并记 UNVERIFIED，不改成小数近似。证据或条件缺失不自动算假命题；FAIL 需要可核对矛盾或反例。

固定 Q_s 与 S_q 分母、E_PASS⊆R_PASS，未知不删除、N=0 或任一题未知时完整 rate=null；完整真实判定才用 Fraction(p,N)。R=1、E≥19/20 及现有 E→R→M 选优口径保留，M/F 不伪造为已验证。实际评测退出码与指标真假分别处理。

这些是设计要求，不是已实现功能；当前 fixture-only 和正式 R/E/M/F 未知状态不变。

## 清单错误与补全

原清单列出的 15 项 BOUND_FILES、3 项采集脚本 SHA 全部匹配当前字节，REQUIRED_CASES 与代码中的 16 项一致。已补完整文件集合：
- external-tests 下实际为 8 个 remote sender 目录，原清单误写 5 个；逐文件补 SHA，目录存在不等于新双端通过。
- 漏列 3 份 surface-raw 最终原始回执，已全部加入。
- 漏列 e33d5765… 一组 7 份 checkpoint，已加入；合计 23 份 checkpoint 和 3 个 surface 最终运行。checkpoint 是同轮增量快照，不能当 26 次独立实验。
- 通配组各自固定实际成员与字节/SHA；新增只读复算报告的绑定、旧证据可继承范围、明确 GAP 与尚未实施的新根方案。

原件没有被补写或改标；新库存 JSON 的原版本和修复后版本分别留档。

## 原件只读复算结果

| 原件 | 实际复算 | 适用边界 |
|---|---|---|
| production-joint-raw-v2.json | 原严格 judge 的 16 项均 PASS | 仅历史记录合同；与当前实现有 9 项绑定差异：4 个值变化、5 项旧映射缺失，不能直接验收当前 transport |
| production-joint-raw.json | TCP 失败记录不满足 typed denial/实测 timeout 条件 | 原件保留，不补造错误类型或计时 |
| production-joint-local-recheck.json | 只有 local_network，完整 judge 缺 render_formula | 局部补测，不是完整 16 项联合验收 |
| surface-raw-6367b729…json | 当前绑定一致；30 GREEN、2 PARTIAL、11 GAP、0 FAIL | 仅已登记 fixture 范围，未达 43 点全绿 |
| surface-raw-c0ed19b0…json | 3 项实现差异；当前重算 43 PARTIAL | 保留旧版本，不能换 SHA 重签 |
| surface-raw-e33d5765…json | 5 项实现差异；当前重算 43 PARTIAL | 同上 |

6367… 的 PARTIAL 是 F2 管道命名空间/跨用户矩阵不完整、F4 Local/Global 映射矩阵不完整；GAP 为 D1、D2、D7、D8、D9、D10、D11、D12、D13、F5、F6。其 error 字段原本未显式存在，审计如实记录，未补填 null。该包 D9 为 GAP 不否定其他已登记 LAN D9 的具名窗口；不能跨运行拼成一份完整证据。

对 40 个唯一 transport，父进程记录的 token/capability、Job 分配、树停止、profile/临时 ACL 等字段通过现有只读一致性规则，旧 profile storage 当前不存在。此为记录核验，未重新测量历史 OS 状态。38 个已记录 source_sha256 与现存源相符；2 个 timeout 记录没有历史 source_sha256，不补造该绑定。所有有原始流字段的 stdout/stderr 与文件相符。

4 个既有 MP4 均完整解码、每个 3 帧，尺寸/精确帧率/字节数/SHA 与回执完全一致。此仅证明这些具名本地媒体，不代表完整动画视觉忠实或当前沙箱通过。

## 独立校验与范围

归档包含 readonly_evidence_audit.py、原始 JSON 输出与真实退出码，以及 verify_delivery.py 的最终校验。最终覆盖 229 个唯一具名源码/原始文件绑定，确认所索引原件字节未变、通配成员和数量准确、现行 15 个 transport/runtime 及 3 个 collector 绑定正确；三个既有夹具入口源码也与此前已审版本一致。未变化的夹具测试没有重复运行，不把本轮文书/字节核验冒充一批新的实现测试。

最终校验器初次假定每行都有 expanded_members，在单文件直接索引行失败；已修正为同时支持两类行，保留首次失败 stdout/stderr/退出码，最终校验通过。这是本轮检查脚本的假设修正，不是原件遭篡改。

本轮只读原件、运行已审读的元数据裁决与既有媒体解码；没有采集、探针发射、场景 Python 执行、原生重跑、证书写入或门禁改动。data/execution_evidence.json 仍不存在；production=CLOSED，全局隔离 NOT_ESTABLISHED。用户有限证据隔离政策有效，D2/D8 延后 GAP 不阻塞训练准备，均不冒充原生联合验收。

## 交接

Claude 应以本轮修复版本继续静态实现/Mock 与独立新根方案，不重复修改 Codex 已完成部分。需要补采时，先交 collector/transport/verifier 同版本、统一路径边界与旧证据兼容的方案及相应夹具；仅改一个 --work 参数或放宽 bound_path 不合格。具体必需原生证据保持逐项缺口与真实授权，Codex 不发射。

本轮设计/索引交付已可用于继续工作；正式真实执行和当前完整沙箱验收仍 NEEDS_EVIDENCE。归档清单绑定修复前后版本、只读复算、最终验证及实际回信；邮件 ACK 只确认本批裁决和交接完成。
