# 数据集入场回信复审（2026-10-03）

基线：c4ef655209fffe6d2df4eb6222d8839b5242a7ec，另含本轮 Codex 输入覆盖保护小修。
最新可见回信：Claude Code msg_1790943163072_153、msg_1790946442963_154。
邮件记载 64→63 条历史修正；当前 HEAD/文件已继续修正至 62 条，本轮结论以当前哈希为准。

## 当前数据复核

- 62 条：数学分析 19、解析几何 11、高等代数 23、概率论 9。
- 全局 ID 实测 62 个唯一值；四个原始 JSON 数组与对应 JSONL 逐对象一致。
- 入场工具当前返回 clean；data/v1/manifest.json 文件哈希校验通过。
- 没有 train/eval/test 冻结验收结论；近重复仍未校准，当前 62 条无动画 code，不代表数学/动画已验收或训练就绪。
- 本轮没有修改真实数据、确认新的许可、训练、下载、安装或上传数据。

## 验证及已修复小项

原全量：167 passed + 29 subtests，6.09 秒。
新增 tests/test_intake_review_guards.py 四条：核心转换同输入拒绝、CLI 路径别名拒绝、报告拒绝覆盖任一输入、新报告正常且输入不变。
旧代码 3 failed / 1 passed；小修后 171 passed + 29 subtests，6.65 秒。

改动仅：
- src/animtrain/dataset_intake.py：src.resolve()==dst.resolve() 时拒绝，--force 也不能覆盖转换源文件。
- tools/dataset_intake.py：report 的输出 resolve 命中任何输入时拒绝，--force 不能绕过。
- 输入覆盖反例全部在临时合成文件上验证；真实 JSONL 前后哈希未变。

命令：设置 PYTHONIOENCODING=utf-8、PYTHONUTF8=1、PYTHONDONTWRITEBYTECODE=1 后执行 .venv/Scripts/python.exe -m pytest -q -p no:cacheprovider。
[probe.py](probe.py)、[修复前](before.json)、[修复后](after.json) 保存当前数据哈希与负向返回值。

## DI1：空输入错误通过（待 Claude Code）

check_intake_file(空 JSONL)、intake_report([]) 均 ok=True/status=clean/exit 0。
新入场接口必须与原数据门禁一致，空输入形成可定位失败。不能由“没有发现问题”推导“已检查合法数据”。

## DI2：跨文件重复 ID 未检测（待 Claude Code）

两份 JSONL 各一条同 ID、不同内容的合成样本，单文件内部均唯一；intake_report([a,b]) 仍 clean。
CLI check 也逐文件检查，未调用跨文件 ID 校验。
当前真实 62 条没有此问题，但工具声称的全局 ID 唯一性尚未实现。需保留双方文件/行号并拒绝重复或冲突，不能静默改 ID。

## DI3：字段结构与正式契约不一致（待 Claude Code）

合成反例 id=["bad"]、problem=["bad"]、scene_spec={"wrong":"shape"} 均 clean。
当前 _is_missing 只检查缺失，不保证 ID 是合法 str/int、正文类型正确、scene_spec 有 objects/steps 列表。
这属于选定数据契约正确性，正式入场前补齐；不提前扩展泛用数据类型。
动画 code 缺失的 candidate/UNVERIFIED 是独立验收状态，不能因入场 clean 就宣称动画验证成功。

## 旧审计快照过期

dataset_audit_2026-10-03-current/summary.json 实际记载 63 条；
calc/linalg/prob 三个 JSONL 的 SHA256 与当前 62 条对应文件不同，geom 哈希仍相同。
因此该目录名虽带 current，内容仍不是最新全量审计。保持旧证据原样，新审计需绑定本轮输入哈希。
本轮只确认入场和文件完整性，未把旧审计数学结论重新认定为当前数据的完整验收。

## 协作与其他状态

已发 Claude Code msg_1790958673855_159、msg_1790958776153_160，交回两个源码文件继续主导 DI1–DI3。
GitHub Animation 的 v0.2.0 预发布已核对存在；上次因自动审批额度无法 push 的动作后来已由协作端完成。
工作区 NEWRELEASE.md 删除和 pyproject 0.2.0→0.1.0 回退为本轮之前的外部改动，未擅自恢复；发布版本一致性需在下一次发布前核对。
本轮小修未提交；不推送未跟踪真实数据。C 类低影响事项维持排期。
