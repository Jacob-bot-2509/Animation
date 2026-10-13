# 动画模型训练项目 修复报告

> 报告期:2026-09-29 至 2026-09-30。项目:D:\Animation Model Training。
> 协作模式:Claude Code 主导实现,Codex 同步审查并处理 CLI/文档细节。
> 全文数字均为实测(测试命令与提交 hash 可复核),未完成项如实标注。

## 一、审查—修复历程总览

| 轮次 | 审查结论 | 问题数 | 修复提交 | 测试结果 |
|---|---|---|---|---|
| 首轮 | BLOCKED(R1–R8) | 8 | b286cd3 | 45 → 60 passed |
| 二轮 | BLOCKED(6 项剩余) | 6 | ace3d33 | 60 → 72 passed |
| 三轮 | BLOCKED(4 项剩余) | 4 | 394bcd6 | 72 → 84 passed + 13 subtests |
| A 组 | 按优先级修复 | 2 类 | 407426c | 84 → 93 passed + 22 subtests |

提交链:28d916b(基线)→ b286cd3 → d6daf61 → ace3d33 → 394bcd6 → 407426c。

## 二、首轮修复(R1–R8,审查 verdict BLOCKED)

| ID | 缺陷 | 修复 |
|---|---|---|
| R1 | split 输出可原地覆盖 pool;四工具无写保护;run_id 可路径穿越 | 统一默认拒绝覆盖(--force 放行);run_id 限定 [A-Za-z0-9_-] |
| R2 | split_manifest 不兼容 Manifest.load;scan 把 split 产物全标 raw | 改标准 Manifest v1;顺带修 rstrip 字符集 bug(train→trai) |
| R3 | 来源/SHA 空仍 ok;坏 JSON 通过;entry.path 可越界 | 越界拦截;缺 SHA/来源/许可证 → quarantine 不默认通过;坏 JSON 报行号 |
| R4 | eval/test 只与 train 比 | 三集合两两比对(ID + 内容哈希双重) |
| R5 | mock GPU 可通过;空 JSON 模型目录通过 | 严格模式:权重文件必须存在且非空;诊断/严格分离 |
| R6 | import os as operating 别名绕过;未验证项宣称通过 | 别名解析检出;math/render 如实标 unverified |
| R7 | answer=0 误判缺失;行号恒为 1 | 仅 None/空串算缺失;报真实源行号 |
| R8 | 缺 env/manifest 路径通过;先保存后校验 | env 必填;hash 必须带路径;先校验后落盘 |

## 三、第二轮修复(6 项剩余)

- R3 路径二次读取:approved 清单贯通全阶段,被拒 entry 绝不再读
- R3 坏 JSON 覆盖 eval/test(不只 train)
- R5 data_manifest 必须真实(unrelated 检查不得冒充);0 字节权重拒绝
- R8 manifest_path 不存在即报错;先校验后落盘(不占 run_id);check 验证 run_id
- R2 split 加 --license,不硬写 internal-generated
- R1 --force 也不得覆盖 pool/plan(逐项 resolve 比对)

## 四、第三轮修复(4 项剩余)

- 坏 JSON 检查按扩展名区分:.jsonl 逐行、.json 整文件(pretty JSON 不误报)
- null/数组/标量行结构化标记 <non-object>,不再 AttributeError
- run_record check 的 manifest 路径语义:显式 --manifest 优先,否则记录内路径
- split 空集合策略:无样本的 split 不写空文件不登记

## 五、A 组修复(REVIEW_BACKLOG,影响数据与评测可信度)

| ID | 问题 | 修复 |
|---|---|---|
| A1-1 | 空 manifest 函数直调可通过 | entries=[] 即失败 |
| A1-2 | source 仅空白可通过 | strip 判断 → quarantine |
| A1-3 | size 登记值与实际不符可通过 | 数据文件 size 比对 |
| A1-4 | null 行只内部标记不报告 | _find_non_object_lines 形成问题报告 |
| A1-5 | problem=[]/solution={} 通过 | 空容器算缺失(0/False 仍合法) |
| A2 | 近重复 top20 截断漏检(实现 bug) | 全候选 Jaccard;自身查询实测 0.042 → 1.0 |

## 六、Codex 并行贡献(已合并,原样保留)

- CLI 加固:make_manifest/check_fields/check_code/data_check(空输入失败、
  互斥参数、输入文件防覆盖、白名单路径语义)
- fs_guard valid_run_id 的 match → fullmatch(换行绕过)
- tests/test_cli_contracts.py、tests/test_code_alias_review.py、测试加固
- README / data README / .gitignore / REVIEW_BACKLOG.md 文档

## 七、遗留项(如实,未完成不宣称)

| 组 | 内容 | 排期 |
|---|---|---|
| B1 | config 实际参数/数据代码版本/seed/env/dirty 快照 | 正式 baseline 前 |
| B2 | 严格 preflight 聚合(L1–L5) | 训练计划前 |
| B3 | 冻结 eval/test 与指标定义、逐样本结果 | 正式对比评测前 |
| B4 | 真实 API/数学/渲染检查与执行隔离 | 执行生成代码前 |
| B5 | 近重复阈值分语言/长度校准(0.7 仍 UNCALIBRATED) | 真实数据隔离验收前 |
| B6 | 冻结产物写保护/原子发布/失败恢复 | 写入正式产物前 |
| C | 长期备忘录(阈值校准方法、split 输出锁等) | 主线完成后 |

训练、模型下载、依赖安装均未执行,需用户另行批准。
