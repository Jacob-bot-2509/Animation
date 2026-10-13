# Claude Code 修复进程独立复验（2026-10-03）

回信：msg_1791005728965_220。稳定审查提交：**1f879d2**；涵盖 9040b19、534ac51、92b6491/7dae434、ada1faf、9c7a8ca。全量独立 **301 passed + 29 subtests passed**（8.86 秒）；真实四组 63 条入场 clean，训练清单四条目问题/隔离项为零。

结论：**修复有明确进展，但 B6/B2/B1/A9 仍需继续修改；B4 只关闭了两项旧故障分支，完整隔离未完成。** 本轮没有接管主实现，仅写临时复现与审查台账。详细残余已发 Claude Code：msg_216、217、218、221、222。不能将“回归全绿”或“待复验”直接改成独立验收通过。

## 已确认的进展

| 项目 | 独立结论 |
|---|---|
| 前轮 Codex 小修 | 9040b19 精确合入；报告输入/冻结/硬链接保护、参考集有效性与全目录 ID 守卫保持 |
| B6 发布预检 | 同一目标重复、已经存在的备份碰撞开始拒绝；清理失败立即返回时保留新内容/journal，没有再自动删掉已无备份的原文件 |
| B2 核心聚合 | 八项必需门禁统一；只传旧四项不能 READY。只报数字没有 records 开始拒绝 |
| B1 配置 | baseline/improvement 缺 config_path 现在拒绝，不再可选跳过 |
| B4 Job 错误 | ERROR_ACCESS_DENIED=5 现在抛 OSError，assigned 不增加；挂入失败 kill+wait，返回 exec_error / job_assigned=False |
| A9 初步接口 | intake 可接收带分类/来源的多解身份，CLI 开始比较候选文件之间的正文重叠；尚未形成一致的逻辑集合契约 |

## B6：仍能丢原文件、丢目标或破坏已提交组（P1）

源码 src/animtrain/publish.py；证据 probe.py / results.json。

| 合成故障或输入 | 当前实际结果 |
|---|---|
| 备份 write_bytes 写入 PARTIAL 后抛 OSError | 恢复仅检查备份存在，用残缺备份替换仍完好的原文件；原文件为 PARTIAL，journal 删除 |
| 清理第一份备份成功，第二份失败，随后默认 recover | 恢复忽略 cleanup 阶段；a 留 newA，b 回 oldB，已提交组被混合 |
| 目标清单同时包含 a 与 a.pub-bak | 返回发布成功的两个路径，但 cleanup 删除第二个目标 |
| 目标正好等于本组 journal | 返回发布成功，但最后删除了实际目标 |
| existed_before=False 的恢复项，其目标随后被有效锁冻结 | 新文件删除分支未调用冻结守卫，冻结文件被删，journal 也删 |
| journal 内容为 {} | 仍报告 recovered=True 并删除，不能称完整 schema fail-closed |
| 回滚第一份成功，第二份 replace 中断，重试 | 两原文件最终还原，但第一份因备份已消费被当不可恢复，永久保留 journal、报告失败 |

继续修改：备份必须完整原子落盘并绑定原始字节哈希，保留逐项阶段；cleanup 阶段只能前滚或无修改拒绝，不能部分回滚；整组目标、备份、journal 命名空间互斥；所有删除/替换均先做冻结检查；完整严格校验非空 journal；根据哈希/恢复状态识别已经还原的文件，允许幂等重试。正式 split CLI 事务接入仍待最终验收。

所有复现都在系统临时目录，没有作用于真实原始文件。现有模块测试没有覆盖“备份写入中途失败”或“目标与另一个备份交叉重合”，因此全绿不能消除这些已确认风险。

## B2：逐条记录仍不是实际资产验收（P1）

当前逐条 input_sha256 使用 canonical_problem_hash，只绑定题干，未绑定 solution、scene_spec、生成 code 等实际动画输入；output_sha256 仅要求非空，没有文件路径或真实产物核对。

两项独立反例的 manifest/data_gate 都通过：

- output_sha256='no-artifact-exists'，没有任何产物文件，资产门禁仍 True。
- 改写 solution 和 scene_spec 后重建正确 manifest，保留旧题干哈希及旧逐条记录，资产门禁仍 True。更新全局清单绑定不能证明逐条输入/输出重新验收。

继续修改：区分题目隔离哈希与完整资产输入哈希；逐项绑定完整输入、真实产物路径/字节哈希/大小及数学/渲染证据所针对的内容。缺产物、损坏或陈旧证据应 UNVERIFIED/拒绝。无需运行真实训练来验证这些守卫。

## B1：代码状态采集与核心缺省仍可假重放（P1）

ada1faf 已加实际文件哈希与配置守卫，但下列独立反例仍返回空问题列表：

1. 记录删除 deleted_a.py，当前删除 deleted_b.py；两边 hashes={}，changed 列表不同却被忽略。
2. git status --untracked-files=normal 将新目录汇总为 new_package/，采集器仅处理 is_file。内部 code.py 改变后两次 dirty 快照完全相同，重放通过。
3. 核心不提供当前 git_commit_now 与 dirty_now，仍可“证明”重放，检查被可选略过。

继续修改：用完整、可无歧义解析的 Git 状态采集所有所需文件，记录删除/重命名与内容；独立比较变更集合和状态；200 条截断或无法采集必须标不完整，不得完整通过；缺可信当前代码状态不能略过。

## A9：逻辑集合与物理文件混淆，组约束未验（P1/P2）

9c7a8ca；eval_probe.py / eval-results.json：

| 情形 | 当前结果 |
|---|---|
| 同一 eval 题目两种 method，存一个 JSONL | exit 0 |
| 相同两条记录分成同一 eval 目录的两个 JSONL | exit 1，误当跨集合同题 |
| 同一 problem_id，solution_id 不同但 method 相同 | exit 0 |
| 同一 problem_id，对应不同题干 | exit 0 |
| 多解记录缺 method | exit 0 |
| 无 id 的复合身份记录进入正式 manifest | intake 没有硬伤，但 validate 返回缺 ID；消费者未统一 |

继续修改：明确 eval/test 角色，按逻辑集合聚合后隔离；eval 内同题多解允许分片，同组题干必须稳定、方法/解法身份必须一致且唯一；所有多解必需字段校验；manifest、资产证据与后续转换统一身份提取。复合身份的字符串分隔符也应无歧义。文档示例分类字段仍需与必需字段一致。

## B4：两项原反例关闭，能力与实际执行限额还需分清

job_probe.py / job-results.json 确认错误5拒绝与 kill+wait 已通过。job_assigned=False 已明确报告，是有效改善。

但本次 job 创建失败、后续能力探针成功时，渲染结果仍报告 memory_limit_mb=2048 同时 job_assigned=False；应让实际执行限额为 None，能力可用性放独立字段，或至少保证所有消费者显式使用实际挂入证据。Popen 后挂入的运行窗口、fs/network 尚未完整隔离；主力回信承认其平台方案待实现。默认不可信执行仍拒绝，本轮没有运行生成代码。

## 验证、范围及后续顺序

本轮中间测试捕获过 GS3 新测试漏 import 的 NameError，主力随后修正；稳定 301+29 已通过，没有代改其测试或降低门禁。本轮仅新增本审查目录的复现/证据，并更新 REVIEW_BACKLOG；不改变主力实现或外部已有审计/版本/发布说明修改。

真实数据只读检查：63 条 clean，manifest-train SHA256 仍 8f1c9b98bfc7c07137645b01555e596f798d750912ab2dd7201290e5569e8353。前轮数据哈希保持。模型下载状态来自主力回信（称其用户已批准、正在下载），本轮没有启动或停止下载，也没有训练、依赖安装或正式 split/freeze。

先处理 B6 文件损坏/删除与恢复状态机，再收口 B2/B1/A9 的可信度契约。低影响 C 类继续延期。既有关闭范围保留，当前剩余不能退回“备忘录以后再修”，也不阻止独立基础设施开发继续。
