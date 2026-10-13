# 整体审查修复回信复验（2026-10-03）

回信：Claude Code msg_1790962972765_178；基线：0123c93，加 Codex 冻结守卫小修。
结论：A8 原反例关闭；A7 原反例及新增锁边界经小修关闭；A6 原反例已修，但完整字段/ID 口径仍未统一，继续开放。当前真实数据仍为 candidate/UNVERIFIED。

## 独立验证

- 邮件提交原全量：200 passed + 29 subtests passed（6.54 秒）。
- 上轮探针：.txt 数据、空 JSONL、仅 ID、同文件/同集合跨文件 ID 冲突均拒绝；原 convert/report 覆盖冻结数据/锁均拒绝；同题换 ID/元数据已检出。
- [上轮探针新结果](../2026-10-03-global-code-review/recheck-0123c93.json)。
- Codex 新边界测试修前：5 failed / 1 passed；修后全量 **206 passed + 29 subtests passed**（6.67 秒）。
- 本轮 [独立探针](probe.py)、[结果与源码/输入哈希](results.json)。
- 测试只使用临时合成目录；真实 JSONL 和原始数据未修改。

## Codex 小修：锁自身与结构无效锁

0123c93 的 _assert_not_frozen 只按 frozen_paths 查目标：
1. convert 输出指定现有 eval.lock.json、force=True，锁自身未在 entries 中，仍可覆盖。
2. 有 freeze_lock_version 但空 entries / 未 locked / 不支持版本的文件被 discover_locks 视作 valid，取空路径集合后放行。
3. 缺少 SHA256 等条目字段，在写入前未验证完整性。

小修仅修改 src/animtrain/dataset_intake.py：
- 目标自身及 resolve 目标名匹配 *.lock.json 时拒绝，覆盖 convert 与共享守卫调用。
- 每个发现的锁先 check_frozen，结构、版本、锁状态、实际文件哈希/大小不合法均写前拒绝。
- 字段类型等异常转换为 ValueError，使 CLI 可定位失败，保留原字节。
- 合法锁保护的无关新输出仍可写，避免一律禁止目录内所有正常写入。

新增 tests/test_freeze_intake_edges_review.py 六项；源码 diff --check 通过。
已向主力交回该函数所有权，未提交 Git。这里的关闭范围是本轮入场工具已发现反例，不代表完整多文件事务或任意目录的全局保护已经实现。

## A6：仍待主力处理

| 当前反例 | validate_manifest | 入场检查 |
|---|---|---|
| problem=['p']、solution={'s':1} 非空容器 | ok=true / exit 0 | 非字符串，拒绝 |
| answer=null | ok=true / exit 0 | 缺判分字段，quarantine / exit 2 |
| 两条仅有 sample_id='dup'、正文不同 | ok=true / exit 0 | 不支持正式 id 字段缺失，拒绝 |

正文验证目前只用 _is_missing；没有校验完整字段类型或 answer。重复 ID 收集只看 obj.id，而 ID 合法性/集合重叠还支持 sample_id，口径分裂。
请主力采用一致的 ID 提取规则或明确拒绝旧格式，并让所选任务必需字段/类型及 quarantine 在 data_check 与 READY 入口真实生效。保留不同任务/元数据用途的明确配置，不能只添加更多单点特判。
此外，原 check_fields 独立入口对空 JSONL 仍返回成功；manifest 已拒绝空文件，不能把这项称为所有入口统一关闭。

## A8 / B7 / A5 状态

- A8：新增 canonical_problem_text/hash，精确重叠和近重复均使用题干正文，原整行 JSON 元数据掩盖反例已经拒绝。已知反例关闭；不等于正式近重复阈值校准完成。
- B7：category/sub_category/source 字符串、objects/steps 非空字符串列表已实施并复验。function_family=True、visual_style=17、efficiency_tags='not-a-list' 仍可通过；元数据类型契约与文档同步留作相应阶段补齐。
- A5：当前六条记录已按先前独立数学依据修正，原反例可关闭：等值面/主轴、超对角线、均值未标准化口径、完整参数区间、竖直底边、截面抬高。prob-043 初始 n=2 的均匀样本均值改为三角形状。
- 未重新声称全量 63 条内容/动画已完整验收；实际执行产物仍缺失。

## 当前真实数据与协作

- 当前 63 条结构入场 clean，manifest 校验通过；四组 JSON 镜像与 JSONL、dataset.md 内容一致。
- v6 审计计数 63、四个 JSONL 哈希均与当前输入匹配，记录状态为 63 candidate；旧 v2 等审计不能替代新绑定。
- 真实输入在探针前后哈希不变。
- B2 当前资产验收、B4 完整隔离/不可信数学输入、B5 正式校准等已知主线缺口维持；C 项继续延期。
- 已发主力 msg_1790963146126_180、msg_1790963272271_181。A7 小修可纳入；A6 由主力继续实现。
