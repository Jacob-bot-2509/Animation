# 全局代码监管续审与小修（2026-10-03）

基线：509ab40 + 本轮 Codex 工作区小修。开始时没有新增修复提交、没有新的未读回信；不将已发送邮件视为主力已接手或已修复。上轮 B1/B2/B4/B6 独立反例重新运行仍成立，范围见 results.json、replay-results.json、job-results.json。

本轮完成了 A9 入口守卫和新发现的 GS6 报告写保护。**284 tests + 29 subtests 通过；真实 63 条数据不变。** Claude Code 继续负责主要结构实现，本轮四个代码文件及三个回归文件已通过 AI Bridge 发出（msg_208–213），尚未提交或推送。

## A9：参考集与全目录身份守卫已修，任务契约仍待实现

修改 tools/eval_test_prep.py，复用 intake_report 的既有入场与全目录 ID 汇总规则：

- 候选样本存在而训练参考目录不存在、无 JSONL、文件为空、坏 JSON、非对象结构时返回失败，不再宣称隔离通过。
- 候选跨文件、训练参考跨文件、候选对 train 的重复 ID 均拒绝，不因题干不同而放行。
- 有 quarantine 时继续允许独立的正文隔离预检，同时显式说明未完成入场完整验收；阈值仍 UNCALIBRATED。
- 候选尚未生成时保留原“未生成、不是检查通过”的只读状态契约；freeze 命令仍拒绝。

新增 tests/test_eval_test_prep_review.py 九项回归：修前八项失败、一项通过；修后全过，原五项 eval/test 测试也通过。旧探针 eval_duplicates / eval_missing_train 现在分别 exit 1。

**A9 未全关：** 文档同题多解字段 problem_id/solution_id/method 与实际必需 id/分类规则仍不一致，eval_schema 探针仍拒绝；test 对 eval 的正式隔离接口尚未接入。当前只有新入口边界守卫通过，不是正式评测集验收。

## GS6 / A7：报告写入可覆盖冻结文件及输入硬链接，已小修

发现 tools/check_fields.py 的 --report/--force 只保护当前输入，没有冻结检查。独立临时探针确认它可以覆盖另一个有效锁覆盖的文件、锁本身、坏锁旁的文件，甚至创建新的 *.lock.json 报告。

第一次接入已有冻结守卫后继续检查 NTFS 硬链接：resolve 不识别同一文件的不同硬链接名，字段报告仍会截断同一冻结文件/锁的底层字节；dataset_intake report 的输入保护也可通过硬链接绕过，原 JSONL 被 Markdown 报告替换。后一情形返回 exit 2 只是候选 quarantine 状态，不能仅凭退出码证明原文件受保护，回归必须核对字节。

本轮修复：

| 文件 | 修改 |
|---|---|
| tools/check_fields.py | 写报告前复用 _assert_not_frozen；force 不绕过 |
| src/animtrain/dataset_intake.py | 对发现范围内的有效锁自身及冻结目标加入 samefile 比较，拒绝硬链接别名 |
| tools/dataset_intake.py | 报告输出对任一输入增加 samefile 检查，拒绝硬链接输入别名 |

新增 tests/test_fields_report_freeze_review.py 七项、tests/test_intake_report_alias_review.py 一项，全部从有意义的覆盖/字节变化反例修到通过；普通非冻结报告 force 覆盖仍正常。未扩展锁发现范围，也未宣称可以自动发现任意远处锁；跨目录显式锁与多文件恢复仍按 B6 验收。

## 仍待主力修复的结构问题

| 项目 | 本轮独立复验 |
|---|---|
| GS1 / B6 | 备份清理失败后回滚丢原文件、重复目标丢原文件、预存备份被删、新文件中断回滚残留、坏 journal 被删、恢复绕冻结保护仍成立；正式 split CLI 尚未消费事务 |
| GS2 / B2 | 三条有效记录 + 自报 1/1 资产证据仍被接受；核心 READY 缺资产/冻结/校准/隔离仍返回 ready=True |
| GS4 / B1 | 不同 dirty 变更仍返回无问题；baseline 无实际配置绑定也能报告完整重放 |
| GS5 / B4 | assign 错误 5 吞错、挂入失败不清理已启动进程、本次无 job 却报内存上限仍成立；fs/network 尚未完整隔离 |

这些已有具体反例，不可因为新增常规测试通过而关闭。B6 原文件丢失与冻结绕过优先；其他项目在对应正式消费/训练验收前修复。没有把主要结构的实现接管到本轮小修里。

## 验证与数据边界

- 全量 pytest：**284 passed、29 subtests passed**，7.86 秒。
- 新增回归仅排版整理后再验：17 passed，1.17 秒；代码逻辑未在全量之后修改。
- data_check --manifest data/v1/manifest-train.json：四条目，problems=0、quarantine=0，exit 0。
- dataset_intake check 当前四个 raw JSONL：63 条，problems=0、quarantine=0、status=clean。
- manifest-train SHA256 仍为 8f1c9b98bfc7c07137645b01555e596f798d750912ab2dd7201290e5569e8353；输入 JSONL 哈希与该清单一致。
- git diff --check 通过；未触碰外部审计文件、版本号或 NEWRELEASE.md 的已有改动。
- 所有新增冻结/故障/硬链接用例只在系统临时目录；没有生成/冻结真实 eval/test，没有训练、下载模型或安装依赖。

source-hashes.json 记录最终小修与数据清单哈希。旧审查目录的修复前证据保留，本目录复制探针并保存修复后结果，不覆盖旧结论。

## 低影响备忘录与协作

C10 核心 fields.check_jsonl 对空文件仍返回 []，当前 CLI 已拦空；不能因其他入口拒空就把这个核心接口缺口关闭。保留为后续调用方接入前处理的备忘录。C5 与正式配置/执行统一仍须 B1 最终验收；本轮不增加维护类修补。

低影响 C 类继续延期，不反复扩大主线。Claude Code 可精确合入本轮四代码文件与三测试文件；下一轮独立验收优先检查 B6 状态机和 B2 真实逐资产证据，不以消息或台账“收口”代替源码与反例结果。
