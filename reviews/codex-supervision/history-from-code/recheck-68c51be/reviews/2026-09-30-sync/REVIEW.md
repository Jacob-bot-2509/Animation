# 同步复审：部分修复，整体 BLOCKED

日期：2026-09-30。Git HEAD：28d916b2f4d42954e2a54f68b31afe050e75b021。
本轮审查的是 HEAD 上的未提交工作区，不是一个新的独立提交。工作区源码哈希见 final_snapshot.json；合成反例运行时哈希见 probe_results.json/source_snapshot。两次快照之间只有 tools/run_record.py 改变，新增 ensure_not_exists 异常友好处理，不改变其先保存后验证的顺序。

## 分工与本轮直接修改
Claude Code 主导实现；Codex 审查、复验并处理小范围细节。未回退他人改动。
Codex 修改 src/animtrain/code_gate.py 的别名调用分支，新增 DANGEROUS_QUALIFIED，覆盖 from os/shutil import ... 与 builtins 别名；新增 tests/test_code_alias_review.py。示例代码只交 AST 解析，从不执行。
补丁前 5 个子样例未检出；补丁后完整测试 65 passed, 5 subtests passed（最终 0.99s）。git diff --check 通过。
重建 REVIEW_REPORT.md、PIPELINE_PLAN.md、RESTART_LOG.md 为 UTF-8 并逐字回读校验；损坏原文保存在 encoding-backup。另一代理创建的 REVIEW_REPORT.utf8.md 保留未改。

## 已确认的改进
- R7：answer=0 不再判缺失；坏行保留真实源行号，两个具体反例闭合。完整字段类型和映射保留验收仍单独进行。
- R4：补上 eval/test 的两两 ID 检测，对应回归通过；近重复校准和完整隔离证明仍未完成。
- R1：默认拒绝已有输出、init 的 run_id 检查已有改善。
- R2：split_manifest 可由 Manifest.load 读取，显式 split 角色已登记。
- R3：缺来源/SHA 的训练条目、坏 train JSON、首轮路径检查已增加。
- R5：严格模式新增模型和数据参数缺失检查。
- R6：import/from-import/builtins 别名子项已修，数学/渲染标记未验证；静态筛查仍不是执行沙箱。
- R8：缺 env 和 manifest 路径字符串开始报告问题。

## 剩余问题与验证结果

| 项目 | 可复现结果 | 主修补要求 |
|---|---|---|
| R3 路径二次读取 | 首轮对 ../outside.jsonl 报越界，但 split_sets 仍调用 _load_lines 读取；outside_read=true | 后续阶段只遍历通过路径/文件检查的清单，不重新遍历全部输入 |
| R3 eval 格式 | 单个 eval 文件为 not valid json，返回 ok=true | 所有 split 统一解析和对象/ID 类型检查；不能只检查 train |
| R5 严格门禁 | mock GPU/模型成功 + unrelated 成功检查仍 ok=true | 校验必需检查名称、证据及 L1–L5 完整性；诊断不得宣称可进入训练 |
| R5 模型完整性 | 三个空 JSON + 零字节 safetensors 被 strict 接受 | 可解析配置、非空且完整的权重/分片证据；不以文件后缀代替完整性 |
| R8 缺真实文件 | env/路径字符串已填，但 manifest_path 不存在，check_record 返回 [] | 缺真实文件失败；验证配置/hash/环境/seed/dirty 证据；CLI 先验证后落盘 |
| R2 来源许可 | split 对未知上游来源统一写 internal-generated | 从上游契约继承授权，不由拆分操作推断；未知进入 quarantine |
| R2 空集合 | train-only 计划产生空 eval/test，数据检查误报相同文件 hash | 明确空集合合法性/阻断原因，不当成样本污染 |
| R1 输入覆盖 | force=True 且 plan 位于 out/train.jsonl，输入 plan 被覆盖 | force 也不得覆盖任何输入或冻结评测；处理路径别名、锁与原子发布 |

合成证据：probe_sync.py、probe_results.json、fixtures。所有越界和覆盖复现均限定本轮新建 fixtures 子树；未读取其他项目，未加载模型，未执行危险代码。脚本使用 exist_ok=False 防止重跑覆盖证据；复验应使用新审查目录并保留正确项目根解析。

静态仍见 tools/run_record.py 在 r.save 之后调用 check_record；check 子命令读取前未验证 run_id。种子/dirty/config hash/L7 固定评测契约、近重复校准/冻结锁、真实 API/数学/渲染仍未完整，不能因本轮测试全绿而取消阻塞。

## 新增端到端记录的限制
只读检查项目内 runs/e2e-review/run_record.json：其 summary.manifest 指向 D:/am_e2e/data/split_manifest.json，超出用户指定动画项目边界；本轮没有读取该路径，也未验证该清单。summary.command 使用另一相对路径，未记录执行 cwd、实际退出码、样本级门禁报告或 dirty 快照，不能据此证明全链路已通过。请主实现者在本项目专用目录生成验证资产，并捕获实际执行结果。

## 交接
msg_1790702095614_108 已通过 AI Bridge 发给 claude-code，含本轮补丁、证据及阻塞修补清单。继续遵守：仅动画项目；不训练、不下载模型、不安装依赖。未自行提交他人未提交改动。下一轮按新提交或稳定工作区快照复验。
