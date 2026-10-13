# B 组独立复审（2026-09-30）

基线：a81223ea46def98b16699fc45ba058b9d7e393ec。审查者：Codex。
本次仅修复 READY 聚合的局部错误；其他主线实现仍由 Claude Code 负责。
源文件 SHA256、完整返回值分别见 [修复前](before.json)、[修复后](after.json)，复现脚本见 [probe.py](probe.py)。

## 结论与验证范围

A1 的 JSON 数据入口已按 95f10f1 明确限制：train/eval/test 注册 .json 均被拒绝；沿已验证 JSONL 范围关闭 A1。
B 组已经有实现，但不能整体标记验收完成。下列错误放行和冻结覆盖必须在对应正式使用阶段前解决，不阻止其他独立模块开发。

- 原始基线：118 passed + 22 subtests。
- 新增 READY 反例：修复前 3 failed / 4 passed；修复后全量 121 passed + 22 subtests，2.32 秒。
- 命令：设置 PYTHONIOENCODING=utf-8、PYTHONUTF8=1、PYTHONDONTWRITEBYTECODE=1 后，运行 .venv/Scripts/python.exe -m pytest -q -p no:cacheprovider；本轮无编码警告。
- git diff --check 通过。本轮没有启动训练、下载模型、安装依赖或执行生成的动画代码。
- GPU/模型检查采用 mock；数学使用本地 SymPy 的简单常量断言；冻结实验全部使用临时合成文件。快照探针还 mock 了数据校验，以单独检验 CLI 是否绑定 manifest hash，不能据此宣称真实训练链路已通过。
- 第三方 RENDER_GATE_VERIFICATION.md/PDF 与 render_gate_assets 保留；其真实渲染证据不覆盖数学假断言、执行权限隔离或完整 READY 链路。本轮未重跑真实渲染。

## BR1：READY 忽略额外失败或被重复检查名遮盖（已修复，待主力纳入）

位置：src/animtrain/preflight.py:98；tests/test_preflight.py:70。
旧实现只用按名称覆盖后的结果检查必需项；额外 render_gate=False 仍 ready=True/exit 0。
同名检查后一次 PASS 还能遮盖前一次 FAIL 或 UNVERIFIED。
现改为遍历所有原始结果检查 FAIL 和 UNVERIFIED，保留必需项缺失检查。
三个反例现在均 ready=False/exit 1；完整合成通过组合仍 ready=True/exit 0。
这里只修聚合逻辑，不代表 CLI 已接齐全部阶段门禁。

## BR2：数学假命题标成已验证（待 Claude Code，B4）

位置：src/animtrain/render_gate.py:80–94。
math_check("Eq(1, 2)") 和 math_check("False") 均返回 ok=True/status=verified，
detail 却明确含 False。当前实现把“能够解析/化简”当成“断言成立”。
先定义接受的断言契约，再区分成立、不成立、无法证明；仅化简表达式不得宣称数学验证通过。
验收至少包含真命题、假命题、带条件/无法证明、非法输入。正式数学质量验收前修复。

## BR3：空锁/未锁状态通过且可以生成空锁（待 Claude Code，B3）

位置：src/animtrain/freeze.py:27、48。
仅 {"freeze_lock_version":1} 或 locked=False/entries=[] 均 check_frozen()==[]；
freeze_set([]) 也能生成后续校验通过的锁。
需校验完整 schema、locked 状态、有效且非空的必需集合、n_files 与条目一致性；
非法结构应形成可定位失败。正式冻结 eval/test 前修复。
目前此模块仅覆盖文件哈希，不能代替 B3 的固定指标、共同样本集合与逐样本结果验收。

## BR4：READY 快照未绑定当前数据，完整门禁尚未接入（待 Claude Code，B1/B2）

位置：tools/preflight.py:40–56。
check_record(rec) 未传当前 manifest_path，因而不核对实际文件哈希。
在其他门禁 mock 为通过的隔离实验中，记录 hash 为 64 个 0，实际文件 hash 不同，CLI 仍 exit 0/READY。
需绑定当前 --manifest、记录的数据版本和运行身份，拒绝不一致。
当前 CLI 没有挂载 render/math/freeze 检查，也未传播 validate_manifest 的 near_dup_calibrated=False。
接入正式训练就绪时需按阶段列出必需项，缺失或未验证应明确 NOT READY，不能凭四项基础检查宣称全链路就绪。
顺带检查 --run-id：当前在验证 ID 前拼接路径，与已有运行记录 CLI 的输入边界不一致。

## BR5：冻结写保护和原子写尚未接到产物发布（待 Claude Code，B6）

位置：tools/split_data.py:95–130；src/animtrain/atomic_write.py。
实测：生成合成 split、冻结 eval.jsonl、修改计划后 split(..., force=True) 成功改写 eval.jsonl；
只有事后主动 check_frozen 才发现哈希变化（见 after.json 的 frozen_split_force）。
已有冻结检查不构成写入前保护。正式冻结产物应禁止 force 绕过，在任何写入前拒绝。
atomic_write 工具函数已实现，但搜索 src/tools 无生产调用；split、freeze、run_record 等仍直接 write_text。
需接入正式写入路径并定义多文件发布失败的恢复行为；单文件原子替换本身不保证整组产物一致。
正式数据/评测产物写入前完成，额外并发优化仍可后置。

## BR6：进程分离尚非生成代码的权限隔离（待 Claude Code，B4）

位置：src/animtrain/render_gate.py:39–68、88。
当前 subprocess.run 禁用 shell 并限时，但未实现文件系统/网络/凭据访问限制，
继承进程环境，RENDER_MEM_MB 未应用。数学 sympify 在主进程内运行，也无计算超时。
本地 SymPy sympify 文档明确提醒其使用 eval，不应接收未清洗输入。
这些是源码/本地文档审查结论，未运行攻击载荷。
执行不可信生成代码之前应提供可验证的隔离与资源限制；尚未完成时明确 UNVERIFIED，并阻断相应执行入口。
可信固定样例的渲染成功不能作为此项关闭依据。

## 协作与后续

已通过 AI Bridge 将初步及具体发现发送 Claude Code（msg_1790783364622_135、msg_1790783514834_136）。
Codex 修改仅限 preflight 核心聚合、其回归测试和本轮审查材料/状态；
数学断言契约、冻结保护、快照与门禁接线由 Claude Code 主导。
C 类低影响整理继续留在 REVIEW_BACKLOG.md，未扩展为当前全项目阻塞项。
