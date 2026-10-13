# 第三轮修复回信复验（2026-10-01）

基线：edb734005e3795b4ef608bc45e5345dc7b8dda3a。
回信：Claude Code msg_1790787355972_144。
结论：有效约定锁的自动发现和固定样例执行已实现；BR5 自动发现失败放行、BR4-b 当前资产证据绑定仍未闭合。

## 验证与范围

- 独立全量：137 passed + 22 subtests，6.93 秒，包含固定可信样例的真实渲染。
- 命令：设置 PYTHONIOENCODING=utf-8、PYTHONUTF8=1、PYTHONDONTWRITEBYTECODE=1 后执行 .venv/Scripts/python.exe -m pytest -q -p no:cacheprovider。
- [probe.py](probe.py) 与 [results.json](results.json) 保存独立负向复现、当前 HEAD、源文件 SHA256。
- 探针全部使用临时合成文件。READY 探针 mock 硬件、数据校验和固定样例执行结果，保留真实快照哈希和锁校验，专门隔离证据绑定逻辑；不是声称实际训练环境已放行。
- 实际近重复校准仍会阻断 READY。没有训练、下载或安装；业务源码未改。
- HARNESS_PARALLEL_RENDER_REPORT.md 在本轮开始前已有外部未提交修改，未触碰。

## 本轮确认的进展

- 不传 --frozen-lock 时，输出目录内有效 frozen.lock.json 能被发现，覆盖被拒绝，全部探针 JSONL 保持原样。
- 显式有效、缺失、损坏锁路径依然拒绝写入。
- preflight 已调用真实 render_check/math_check，输入分别为固定 MathTex("x^2") 场景和 Eq(2+2,4)。不再只检测依赖存在。
- 无任何发现的锁时 freeze_gate 失败，正确 manifest 哈希也不会独自放行。
- BR2、BR4-a、BR6 默认阻断等前轮通过项无回退。

## BR5 剩余：自动发现失败时仍放行

位置：src/animtrain/freeze.py:60、82。

1. omitted_corrupt：先冻结 eval，再把输出目录 frozen.lock.json 改为坏 JSON，不传锁参数。_is_freeze_lock 返回 False，锁被跳过；split(force=True) 成功改写 eval.jsonl、train.jsonl。
2. omitted_nonstandard：freeze_set 支持在同一目录创建 freeze.json，但 discover_locks 只搜 *.lock.json；不传参数也成功改写上述两个文件。

有效约定锁的旧反例可关闭，但不能据此关闭全部冻结写保护。
需要锁创建与发现采用同一受支持约定：可强制规范命名/持久登记，并对已认定的冻结标记损坏保持拒绝。不要求无限搜索整个磁盘。
验收必须覆盖漏参+坏锁、锁名约束，并断言拒绝前所有输出未变。正式冻结产物写入前完成。

## BR4-b 剩余：证据未对应当前资产

位置：tools/preflight.py:80–100。

探针 snapshot.matching_hash：当前哈希正确、其他隔离条件通过，但无锁，exit 1。
接着只冻结无关的 unrelated.txt，生成 unrelated.lock.json；其他条件完全不变，snapshot.unrelated_lock 变成 READY/exit 0。
这说明当前 freeze_gate 只要求某个发现的锁校验通过，没有检查锁覆盖当前 manifest 的 eval/test 集合。

同时 render/math 始终验证固定样例。它们证明执行环境能工作，不能证明当前数据/代码产物已通过相应验收。
正式 READY 应消费与当前资产哈希/集合绑定的验证证据，并确认完整冻结覆盖；仅无关锁、部分覆盖或固定样例不能替代。
如正式证据入口尚未完成，可保留固定样例作为环境诊断，并让正式 READY 明确 UNVERIFIED。无需为了完成本项提前执行不可信代码。

## 后续

已发 Claude Code：msg_1790787525950_145，附反例与明确验收边界。
上述问题属于前轮 BR5/BR4-b 的剩余条件，不是新增全项目阻塞。完整隔离、正式校准、多文件恢复仍按原 B 组阶段验收；C 类低影响事项不变。
