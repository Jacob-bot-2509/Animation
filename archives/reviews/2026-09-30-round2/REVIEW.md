# ace3d33 第二轮修复复验

结论：本轮列出的具体修复大部分验证通过；全局验收仍 BLOCKED。
基线提交：ace3d33。Codex 仅修改 tests/test_review_round2.py 中两个不充分的测试，并新增本目录证据，未改核心实现。

## 验证通过
- 被拒的真实越界文件不再二次读取，outside_read=false。
- 损坏 eval JSON 被按行报告；无关检查不能冒充严格模式的 data_manifest。
- 零字节权重文件被拒；显式传入不存在的 manifest_path 会报错。
- 未指定许可证的 split 输出保持空值并进入 quarantine。
- --force 无法覆盖输入 plan，使用 pool/out 分目录样例确认。
- run_record 缺配置失败不落盘，不占用 run_id。
- 项目内真实 CLI split → data_check 成功：train/eval/test 各一个合成样本，明确 internal-generated，两个退出码均 0。命令、cwd、stdout/stderr 存于 probe_results.json/e2e_cli。

完整测试：72 passed, 5 subtests passed in 1.05s。
测试加固：越界测试原文件实际位置与 entry 不符，现为真实存在的 sibling 文件并拦截 Path.read_text/open；输入保护测试原先提前命中 pool/out 同目录规则，现分目录并逐字验证 plan 不变。这两项改动保留给主实现者合并。

## 尚需修复的具体问题
1. [P1] 合法多行 .json 被当 JSONL 逐行解析而误拒：validate.py 的 _find_bad_json_lines 被用于两种格式。pretty.json 的合法对象产生三条解析错误。这是 ace3d33 对坏行检查扩展带来的兼容性回归。应统一按后缀解析 .json 整文件、.jsonl 逐行。
2. [P1] 合法 JSON 标量 null 触发 AttributeError，未生成结构化 quarantine/失败报告；_load_sample_ids 直接调用 obj.get。数组、ID 类型等也需统一校验，不能只捕获 JSONDecodeError。
3. [P1] check_record(r) 不传 manifest_path 仍不检查 summary.manifest 所指文件，即使该文件不存在也返回 []。CLI check 的 --manifest 可选，因此默认路径仍绕过真实文件验证。应默认解析记录中清单位置并核验，明确相对路径基准。
4. [P2] train-only 计划产生两个空 eval/test 文件，仍以相同空文件 hash 报污染；应明确空 split 是允许还是缺必要集合，并报告对应原因。

以上证据在 probe_results.json。使用旧英文结果键便于逐轮对照，例如 bad_eval_accepted 的当前 ok=false 表示问题已修；不是说当前仍接受。

## 全局门禁仍未完成
strict preflight 尚未聚合完整 L1–L5，模型检查未证明配置/权重分片有效；L5 种子、配置内容哈希、dirty/代码快照与 L7 固定评测契约待补。近重复 0.7 未校准、实际 API/数学/渲染未验证，冻结评测锁/原子发布仍待验收。正常合成样例 E2E 通过不代表训练就绪。

所有本轮证据在动画项目内；未读取其他项目、未训练/下载/安装。回归测试使用标准临时目录，未删除或覆盖原始项目数据。脚本默认拒绝复用已有 fixtures，以保留历史证据。
