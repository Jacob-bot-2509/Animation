# 全局代码监管复审（2026-10-03）

独立审查基线：新增模块 fdacdd9、8c15d4d、62a4ee2；新增重放 2ab3d08；稳定测试 f741261，台账更新 ec824fe。并行工作区的具体源码 SHA256 保存在 results.json / replay-results.json 中。审查覆盖发布与恢复、资产证据及 READY 聚合、eval/test 入口、运行快照与新后端契约；既有数据门禁通过回归测试复验。

结论：**常规回归通过，B1/B2/B4/B6 尚不能关闭；新评测入口存在错误放行。** 问题已通过 AI Bridge 发给 Claude Code（msg_202、msg_204）。追加内存隔离复审见 GS5。以下问题属于主线正确性与数据完整性，不列入 C 类延期。未训练、未下载模型、未安装依赖、未生成或冻结真实 eval/test。

## GS1 / B6：发布失败与恢复可能丢文件（P1）

位置：src/animtrain/publish.py:29、:56、:90–105。

| 独立合成反例 | 实际结果 |
|---|---|
| 两个原文件都写完，删除第一个备份成功，第二个备份清理抛 OSError | 异常路径试图回滚，但第一份备份已删；a 被删除、b 恢复为 oldB，journal 也被删 |
| 同一目标重复登记，再让后续目录目标写入失败 | 原文件消失；没有输入去重，第二次写入覆盖第一次的原备份 |
| 新目标不存在，但同名 .pub-bak 文件已存在；不指定 force | 发布成功并删除预存备份文件，没有碰撞守卫 |
| 模拟中断后只有新目标、没有备份，执行默认恢复 | 新目标残留，journal 删除，报告 recovered=True；整组没有回到原状态 |
| 损坏 JSON journal | 报 recovered=True 并删除 journal，恢复依据丢失 |
| 临时目录内有效冻结锁覆盖目标，执行 journal 回滚 | 冻结目标被替换为不同内容；recover 路径不复用写保护 |

需要区分未提交与已提交清理阶段；持久化原文件是否存在、原/新内容哈希、动作状态和提交标记。提交后的清理失败不得进入需要已删备份的回滚。写入前统一拒绝重复/别名目标、备份碰撞与不合法事务路径；恢复前完整检查 journal、备份与冻结保护，异常保留可恢复证据。自动恢复必须可重复执行。

publish_files / recover_publish 目前未被正式 split CLI 消费；tools/split_data.py 仍逐个 atomic_write_text。模块修完后还需验证正式入口接入，不能从六项模块测试直接声称整条发布链已收口。

## GS2 / B2：资产覆盖自报与核心门禁缺失（P1）

位置：src/animtrain/preflight.py:56、:59、:150。

1. 三条合法合成训练记录组成 manifest，validate_manifest 返回 exit 0；仅提供 manifest_sha256 和自报 n_total_records=1 / n_verified_assets=1，没有逐资产数学/渲染记录，check_asset_evidence 仍返回 True。它比较的是两个自报数字，没有核对真实样本数量、身份与验收结果。
2. 库入口 run_preflight(ready=True) 在模拟 GPU/模型存在并只提供 data_manifest/run_snapshot 时返回 ready=True；asset_evidence、freeze_gate、near_dup_calibrated、exec_isolation 全部缺失。CLI 会追加这些门禁并阻断，但核心必需列表只有四项，未来调用方仍可绕过。

验收应绑定当前 manifest 与真实输入文件哈希，核对实际样本清单、唯一身份、逐条真实数学/渲染结果以及当前产物哈希。计数只能由逐条证据推导。所有就绪入口统一要求必要门禁；缺失或结构不可验证必须 NOT READY / UNVERIFIED。合成探针的 GPU/模型结果仅用于复现聚合逻辑，不代表实际环境就绪。

## GS3 / A9：新评测入口与既有契约不一致（P1/P2）

位置：tools/eval_test_prep.py:60–106；EVAL_TEST_PREP.md §3.5。

| 情形 | 实际结果 |
|---|---|
| 候选存在，--train-dir 指向不存在目录 | train_lines 为空，exit 0 且报告“与 train 隔离检查通过” |
| 两个候选文件使用相同 ID、不同题干 | 分别 check_intake_file，没有汇总，exit 0 |
| 文档 eval schema 使用 problem_id/solution_id/method，不提供 id | 通用 intake 拒绝“缺关键字段 id”；文档例子还缺必需分类字段 |
| 阅读跨集合检查逻辑 | 只比较 train 正文哈希/shingle，没有跨 train ID 检查，也没有 test 对 eval 隔离入口 |

需要统一多解记录的独立行 ID、problem_id、solution_id、method 契约，允许同题多解同时验证题干一致与方法身份；复用全目录重复 ID 检查。训练参考缺失、为空或不可验证时不能宣称隔离通过；正式 test 验收还须隔离 eval。近重复当前仍 UNCALIBRATED，本工具不能代替正式隔离验收。

status 对冻结锁只统计文件存在，没有 check_frozen，且有 JSONL 时固定输出“未冻结”，随后又输出锁存在。这一状态文案/真实锁消费归 B3/C9，在正式冻结状态消费前补齐；当前真实 eval/test 仍未生成，没有把这些临时合成样本混入数据目录。

## GS4 / B1：“完整可重放”仍可能假通过（P1）

位置：src/animtrain/run_record.py:107–142；tools/run_record.py:153–183。

- 记录 dirty.clean=False、changed=['src/a.py']，当前同样 clean=False 但 changed=['src/b.py']；verify_replay 返回空问题列表。它只比较 clean 的布尔值，没有比较变更集合，更没有绑定未提交文件内容。
- baseline 记录仅 config={'learning_rate':0.1}，不提供 config_path；配置绑定校验全部跳过，仍返回空问题列表。CLI 缺 config.file 也会走此路径并打印“完整可重放”。

实际训练记录缺少可信代码状态或配置文件依据应拒绝/UNVERIFIED。可选择拒绝未经快照的 dirty 状态，或保存并核对完整代码差异及必要未跟踪文件哈希。实际训练配置必须绑定，不能因参数缺省而跳过。字段存在与 git commit 相同不证明当前代码相同。

## 已验证改善与边界

- f741261 稳定全量：**263 passed + 29 subtests passed**，7.73 秒。首次运行正逢 C2 修改产生 3 fail，稳定轮已消失，不能将并行中间态当未修复结论。
- C2 已默认拒绝空 split；显式 --allow-empty 保留旧场景；空文件不再误报同哈希重叠。C12 的 GPU 查询超时已加入，其他效率项仍延期。
- B4 新增数学 AST 预检、受限命名空间和环境脱敏；默认不可信渲染仍拒绝。该时点 memory/network 隔离未实现（后续 job 新改动见 GS5），CLI exec_isolation 正确阻断。此轮没有执行攻击表达式或不可信代码，也没有据此声称完整安全隔离已通过。
- backend 仍是拒绝未批准真实操作的接口骨架；没有模型/训练运行。本轮不评价实际后端质量。
- 真实 63 条数据未改，原候选入场/正文防泄漏已知反例保持关闭。新入口遗漏单独登记 A9，不能扩大旧关闭结论。

## GS5 / B4：新内存隔离的失败分支与执行证据（P1）

追加基线：4a9ea51 / 509ab40。位置：src/animtrain/win_job.py:84–98；src/animtrain/render_gate.py:74–117、:186–213。

| 纯 mock 反例 | 实际结果 |
|---|---|
| AssignProcessToJobObject 返回失败，错误码 5 | 没有抛错，仍把句柄加入 assigned；新 job 没有接管进程 |
| 已 Popen，随后 job.assign 抛 OSError | 返回 exec_error，仅关闭 job；没有 kill、wait、communicate 或 job.terminate 已启动的进程 |
| 本次渲染 job 创建失败，后续能力探针可创建 | 仍报告 rendered 且 memory_limit_mb=2048，实际该进程从未挂入 job |

这些探针没有启动生成代码或任何真实 mock 子进程。正常 job 创建/回读与超限测试通过，不能覆盖失败分支。错误 5 不能证明其他 job 带同一内存上限，必须如实拒绝。统一异常清理与回收应在 finally 中保证；报告必须基于本次创建及成功挂入的 job，不能用另一次能力探针取代实际执行证据。

Popen 后才 assign 还存在子进程先运行/派生进程的窗口；该窗口是源码检查指出的风险，尚未用进程抢跑实验量化，不能当已完成整树隔离。执行生成代码前需要挂入后启动或等价约束。fs 仍只是 cwd，network 未隔离，默认不可信代码仍应拒绝。

最新稳定全量：**267 passed + 29 subtests passed**，6.82 秒；未解决 GS1–GS5 的独立反例。新增 job_probe.py / job-results.json 保存这三项故障分支及源码哈希。已发 Claude Code msg_207。

## 复现材料

- probe.py / results.json：11 项发布、READY 与评测入口探针。
- replay_probe.py / replay-results.json：2 项重放探针。
- 所有写入、有效冻结锁与故障注入仅作用于自动清理的系统临时目录；不存在真实 split/freeze/训练操作。
- 探针不以退出 0 表示被审查模块已经通过；应逐项比较 expected 与实际字段。源码哈希用于识别修复前后的变化。

后续先修可能导致文件丢失/冻结覆盖的 GS1，再落实 GS2/GS3/GS4/GS5 的错误放行守卫。Claude Code 继续主导实现；Codex 独立验证同一反例及跨入口回归。C 类低影响事项按原排期保留。
