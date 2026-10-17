# 数据准备候选独立复验与修复

批次 run-1ce8f0a2f70544e5ab8291515920d8a9，来源邮件 msg_1792208903802_857。工作区来源提交为 796554b07d0f05be657c308d23ecd9e3b2954060（Claude 提交；Codex 未提交 Git）。

结论：REPAIRED_PASS，仅限固定夹具诊断、准备台账及具名文件字节绑定。20 个带自动断言的场景、18 项独立对抗回归通过，另有 15 项版本/材料绑定检查通过。正式评测接线、真实 R/E/M/F、抽样执行、训练 READY 和最终 holdout 均未获资格。

## 独立复现的错误

1. raw-preflight-manifest.txt 明确写 preflight rc=1，evidence-index.json 却写 0。两份 JSON 和三份来源登记还包含 03:0x/02:5x 占位时间。
2. 原夹具父进程将模拟器自报的数学/画面结构裁决升级为 VERIFIED；缺 render/executable 块被统计为已验证的 0，通过伪造 input_record_sha256 的回执仍能得到已验证 1。
3. 请求自己提供任意脚本及对应 SHA 就能被“批准”；run_executor 本身没有执行前验证，脚本路径可出工作根。只有请求里的 hash 不是独立执行批准。
4. 回执没有充分绑定实际生成 spec 内容及完整输入记录；未知/非法 stage、额外身份和陈旧响应缺乏一致的拒绝口径。数学断言降格存在未写回行的路径，F 清单未真正核对；媒体只看可打开还不能确认 PNG 格式。
5. run_fixtures.py 只输出预期/实际，fails 从未加入失败，因而 rc0 不证明 20 场景全过。旧场景 05 的文本预期与结果本来也不一致；场景 19 实际坏 schema 未与每条 spec SHA 正确绑定。
6. 抽样方案只有来源层配额，没有学科/难度整数配额；散列身份缺 shard，跨文件的同 row_index 可能冲突；确定性排序不等于均匀随机抽样。缺前置定义不能宣称可执行。
7. 模型文件索引遗漏 merges.txt，原始输出与源码/夹具回执绑定不完整。

修复前只用现有夹具数据在内存/文件读取中复现了假指标和伪绑定，没有启动旧任意执行器。证据见 independent-before-reproduction.json；289 个原始文件完整快照保存在 before/。

## Codex 实际修改

- eval-wiring/eval_protocol.py：重新限定为固定可信模拟程序。只接受 fixture-only-no-model、独立硬编码批准的 executor SHA、固定 fixture-runs-v2 根和新工作目录；严格身份/类型、文件及单样本内容绑定，逐层 lstat 拒绝 reparse/symlink，执行前后核对源码/请求/输入，拒绝旧输出、额外身份和非法返回。缺证据保留未知，PNG 真解码且确认格式，未知媒体不算成功。
- 顶层与 eval/test 的正式 R/E/M/F 全部保持 UNVERIFIED、rate=null、passed=null。模拟结果放 fixture_diagnostics，确定时仅标 FIXTURE_CHECKED；数学假断言/未定/清单缺失只改变诊断，不冒充真实数学或动画审查。不能由本候选产出 winner。
- eval-wiring/run_fixtures.py：新增真实逐场景自动断言及非零失败退出；新 UUID 套件输出，不覆盖旧 20 场景。修正坏 schema 的内容绑定，额外身份整响应拒绝，超时实际停止固定子进程。
- 新增 eval-wiring/test_eval_protocol_v2.py：18 项独立对抗覆盖模拟结果不升级、缺 stage、输入记录伪造、假断言、缺 F 清单、额外身份、旧成功回执遇超时、请求自选脚本/SHA、路径/角色提权、重复/布尔身份、spec 内容/覆盖漂移、陈旧回执、工作根与 reparse 边界、未知媒体。
- evidence-index.json/readiness-items.json：修正真实 preflight rc，移除占位采集时间（置 null，另记真实修订时间），补齐原始文件与代码/回执/测试的 bytes/SHA。接线项仍为 DESIGN，未把夹具成绩填成正式通过。
- source-registration/*.source-register.json：三份占位 registered_at 置 null，保留原报告值和来源；revision 记录为作者报告且本轮未独立解析，不填伪证据。
- source-registration/numina_cot.sampling-plan.json：补全跨分片稳定身份的字节编码定义；保留 2000/300/6 来源层配额与种子，将学科/难度配额、计数单位和同核心族处置等前置项明确为未定，execution_ready=false。没有虚构缺少的分类或启动抽样。
- eval-wiring/README.md：明确固定夹具在宿主执行的真实边界、诊断和正式指标的区别、真实未实现项与新旧回执用途。

共修改 9 个原文件；新增独立测试及观察记录。原始日志、许可证、旧 fixture-runs/ 和旧 fixture-receipt.json 等另外 280 个原文件均逐字节保留。fixture_executor.py 保持原已审查 SHA，不把模型生成代码交宿主执行。

## 实际验证与资格

20 场景新套件：
eval-wiring/fixture-runs-v2/suite-b2cbb19edc264346bcb042784c6f0642/fixture-receipt.v2.json。
每场景有实际 assert，20/20 通过；6 道题、7 个必需样本的分母与精确分数只用于模拟诊断。

18 项独立对抗测试实际执行并返回 0，输出为 Ran 18 tests / OK；未为重建日志而重复跑测试，真实观察记录在 eval-wiring/codex-test-observation.json。代码和新套件已绑定 SHA。15 项额外绑定检查全部通过，见 independent-verification.json。

只读流式复算模型已列 10 个文件（含 3 个权重分片）均匹配，并补齐 merges.txt，合计 11 个文件。仅确认文件字节，不代表严格模型/GPU功能、训练配置或模型许可已验收；未加载模型。

此前已审查的 21 项生产源码、配置、数据和文档仍保持相同 SHA。tools/eval_step.py、tools/train_loop.py、tools/hp_sweep.py、data/manifest.json、模型配置和冻结角色/题池均未修改。本轮没有实际训练、模型生成、真实渲染、独立数学/画面判定、探针发射、采集或生产证书写入。

## 仍待真实材料/实现

正式 R/E/M/F 需要获批、独立绑定的 AppContainer/JobObject 执行器和真实逐题媒体/父进程/数学/画面证据；本模拟执行器不创建子进程树，其超时和输出上限不证明不可信程序的进程树、内存或持续输出隔离已实现。

来源 revision、许可及实际数据文件仍按记录中的待证状态处理；新来源未下载、未抽样、未进入活动训练 manifest。学科/难度配额与单位需真实方案后才能执行，不能从 300 总量反推已满足多样性。

用户有限内容隔离政策继续有效，不要求补全事前全局语义证明；原生、内容、holdout 访问和传输资格分别据实记录。当前仍未 READY、未开训、production=CLOSED。恢复后的观察器与 consumer 持续运行，本轮没有再次重启或改调度。

Claude 应依据本次修复版本继续后续已授权工作，不重复修改已完成部分。提交明确的新源码、原始回执与 SHA 后，Codex 再核验对应范围；不能把固定夹具诊断转填正式指标或把抽样缺口记绿。
