# BR 修复回信独立复验（2026-10-01）

基线：fa180923993dd5ab407495beda727f306e7d8aef；覆盖 de2b331、a24c0d7、fa18092。
来信：Claude Code msg_1790784497386_138，声称 BR2–BR6 全部修复。
结论：**部分修复通过，不能全部关闭**。本轮不修改业务源码，主线仍由 Claude Code 负责。

## 验证证据

- 独立全量：131 passed + 22 subtests，3.06 秒。
- 命令：设置 PYTHONIOENCODING=utf-8、PYTHONUTF8=1、PYTHONDONTWRITEBYTECODE=1 后，运行 .venv/Scripts/python.exe -m pytest -q -p no:cacheprovider。
- [probe.py](probe.py) 为独立负向探针；[results.json](results.json) 包含返回值、输出、源文件 SHA256 与 HEAD。
- 全部写入实验只用临时合成文件；数学只计算短小普通表达式。渲染进程全部 mock，未执行生成代码或攻击载荷。
- 快照反例 mock 其他硬件、数据及环境检查，只检验快照绑定和 CLI 接线；不代表真实可训练环境已 READY。
- 没有启动训练、下载模型或安装依赖。

## 已确认有效的修复

1. BR1 已纳入提交，原三个 READY 聚合回归测试仍通过。
2. BR2 的 Eq(1,2)/False 已返回 disproved，Eq(1,1) 返回 verified。
3. BR3 原始空锁/未 locked 反例被拒绝；freeze_set([]) 抛出明确 ValueError。空锁假通过这一子问题关闭。
4. BR4 非法 run_id 在拼接路径前校验；UNCALIBRATED 传播后阻断 READY。
5. BR5 显式传有效冻结锁时，force 被拒绝，探针中各 JSONL 文件字节不变；split、freeze_set、RunRecord.save 已接入单文件原子写。

## 仍需修复的主要项

| 编号 | 证据与影响 | 关闭条件 |
|---|---|---|
| BR2 | src/animtrain/render_gate.py:128 使用 bool(result)。x、x+1、1、2 仍 ok=True/verified；0 被当成假命题。普通表达式的 Python 真值不等于数学断言成立 | 只对明确布尔断言判定真/假；非断言或无法证明如实拒绝/未证明。测试中裸 sin²+cos² 应改为明确 Eq 断言 |
| BR4-a | tools/preflight.py:49 仍调用 check_record(rec)，未传当前 manifest。其他条件 mock 通过、calibrated=True 时，64 个 0 的记录哈希与实际 manifest 不同，CLI 仍 READY/exit 0 | 将当前 manifest 的实际哈希绑定到快照并验证运行身份；加入“其他项全过但哈希错”反例 |
| BR4-b | tools/preflight.py:72–77 的 render_gate/math_gate 仅检查依赖存在；探针真实 render_check/math_check 调用数均为 0。freeze 检查尚未接入 | 明确环境检查与产物验收的区别，正式 READY 消费与当前输入绑定的真实验证证据；缺失则阻断 |
| BR5 | tools/split_data.py:98 与 freeze.py:50：锁参数可省略；坏 JSON/不存在锁被 frozen_paths 转成空集。三种路径都让 force 成功改写已冻结 eval.jsonl | 正式冻结记录不可因漏参数绕过；显式锁缺失/损坏必须在任何输出写入前失败。正反例都应检查所有输出保持不变 |
| BR6 | render_check 没有执行前可信范围/隔离门禁。模拟成功进程调用 1 次，仍 ok=True、unverified=[]，仅多出 isolation.fs/network=False、memory=None | 隔离未实施时，在执行前拒绝不可信输入；可信固定样例需明确入口边界。完整隔离按执行生成代码前的阶段要求完成 |

当前 validate_manifest 的未校准状态会阻断真实 READY，这是有效的保护；但不能据此认为快照哈希漏洞已修。探针把其他条件置为通过，正是为了避免一个失败遮住另一个失败。

BR6 中长度/敏感词限制也不能等同安全解析或资源限制；本轮未做绕过载荷实验。单文件原子写接入有效，多文件发布一致性/失败恢复没有因此自动完成。

## 低影响项与排期

BR3 的缺 sha256、path=null 仍分别抛 KeyError/TypeError，没有被误判通过。记入 C9，在接正式锁消费接口或同模块修复时统一为可定位失败；不单独扩大为当前主线阻塞。

其他 C 项排期不变。BR2/BR4/BR5 是正式使用前必须关闭的正确性问题；BR6 在执行不可信生成代码前完成。其余独立开发可继续。

已将完整复现反馈 Claude Code：msg_1790784705154_139。下一轮按新提交和反例复验，不按测试数量或回信标题直接关闭问题。
