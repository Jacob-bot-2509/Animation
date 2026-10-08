# 第四轮修复回信复验（2026-10-01）

基线：cd9fff6094b8fe176225c6a0882bec36ca23d243（含 a4eb3b9），加 Codex 工作区小修。
项目现位于 D:/Animation-Model-Training，原带空格路径已不存在。
回信：Claude Code msg_1790789480769_147。

## 本轮结论

BR5 已知冻结写保护反例在约定锁命名与发现范围内关闭。
BR4-b 的当前 manifest 冻结覆盖/哈希绑定部分已通过；Codex 补上了缺少绑定哈希时错误放行的小遗漏。
剩余原问题是正式 READY 缺少当前资产验收证据门禁，固定样例仍被当成验证结果。完整隔离/正式校准等按阶段继续，不等于当前能力已验收。

## 改动与验证

- 原基线全量：143 passed + 22 subtests，6.66 秒。
- 新增 tests/test_preflight_evidence_review.py，直接调用 preflight CLI，覆盖 matching、missing_binding、wrong_binding、unrelated、partial、corrupt、no_lock 七种情况。
- 修复前 missing_binding 子测试失败：freeze_gate 在没有 manifest_sha256 时仍称绑定成功。
- Codex 修改 tools/preflight.py：meta 缺有效非空字符串 manifest_sha256 时记录失败，禁止作为冻结证据；其余对照行为保持。
- 修复后全量：144 passed + 29 subtests，7.08 秒；git diff --check 通过。
- 测试命令：设置 PYTHONIOENCODING=utf-8、PYTHONUTF8=1、PYTHONDONTWRITEBYTECODE=1 后运行 .venv/Scripts/python.exe -m pytest -q -p no:cacheprovider。
- [probe.py](probe.py) 捕获 CLI 集成结果并独立验证冻结写入；[results.json](results.json) 包含完整 HEAD、当前源码 SHA256 和返回值。

## 关闭范围与证据

| 项目 | 结果 |
|---|---|
| 有效约定锁漏传参数 | 自动发现并拒绝，原产物全部不变 |
| 坏 JSON 锁漏传参数 | 标为可疑锁并拒绝，原产物全部不变 |
| freeze.json 非规范锁名 | freeze_set 在创建时拒绝，原产物不变 |
| 无关锁/部分覆盖/无锁/坏锁 | freeze_gate 均失败，CLI exit 1 |
| 当前 manifest 绑定错误/缺失 | 均失败，CLI exit 1；缺失分支为本轮 Codex 小修 |
| 全覆盖且正确绑定 | freeze_gate 通过，未被错误拦截 |

这些结论只覆盖已声明的 *.lock.json 和发现范围；跨目录场景仍需按接口传显式锁。不宣称文件系统级不可变或完整多文件事务。

## 仍待关闭：资产验收缺失必须明确阻断

NEXT_CYCLE_PLAN.md 与回信称固定样例是环境诊断，但当前 tools/preflight.py 输出仍用 render_gate/math_gate 与“真实证据”，且没有当前资产验收证据的必需项。
probe 的 matching 情况中，只有绑定正确的冻结证据，其他外部门禁 mock 为通过，即 READY/exit 0；固定样例的输入不来自当前资产，也没有当前资产验证报告输入。

该隔离探针不声称真实训练已经被放行：实际近重复校准等仍阻断。
但不能靠另一项尚未完成掩盖当前门禁缺项。
当前阶段最小修复即可：固定样例明确标记环境诊断；正式 --ready 在资产验收入口未实现/证据缺失时返回 UNVERIFIED/NOT READY。真实报告接入随下一周期进行，不要求现在训练或执行不可信代码。

## 协作与范围

业务小修仅 tools/preflight.py 的强制绑定判断，新增测试及本轮审查记录；未提交 git。
已通知 Claude Code 接回该文件继续主导剩余门禁实现。
所有写入反例使用临时合成文件；CLI 测试 mock 硬件、数据校验与固定 smoke，以隔离真实快照/冻结逻辑。
全量测试包含原有可信固定样例渲染；无训练、模型下载或依赖安装。C 项继续原排期。
