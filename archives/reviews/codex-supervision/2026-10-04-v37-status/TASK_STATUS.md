# Claude Code 任务进程与 v3.7 复核

采样：2026-10-04T17:37:29.848558+08:00（北京时间）。HEAD `4456749ae6b8f405928826cf84c503f9618b1fda`，文件脚本 SHA `b5e01edc410d61364a2460deca8fdf96a0e6a97488525ea4096e4000fb5f318e`。

## 当前在做什么

Claude 在 msg_365 明确答复：**当前无本地任务，处于修订回交、等待复核阶段**。最新回交 v3.7。实际进程树仍是两个 claude.exe：PID 45116、27720（父进程 VS Code PID 6984），各带 conhost PID 44984、40172；没有原生文件验收、Manim、TeX 或 FFmpeg 作业。

两个会话在运行不等于任务正在计算；本轮没有证据表明进程卡死。原生验收尚未启动，生产门禁 CLOSED。11 个核心/门禁文件均未偏离保存基线。

## 本轮独立复验

v3.7 同一快照内存模拟确认：24/24 内置自检、24/24 拒读原始泄漏输入均通过；正常证据保存路径/终端 JSON 已一致，所有保存路径失败时 PASS 关闭、FAIL 保留。

但完整写入故障矩阵的 64 组组合中，**16 组仍存在保存文件声明路径错位或终端不一致**。外层处理候选路径时仍调用带自动 fallback 的 `_write_json`，导致先留下“实际备用文件、内容却声明主路径”的记录；重试阶段主路径恢复或备用写入失败也无法保证所有最终记录一致。这是前轮证据写入问题的残余，仍阻断原生验收审核。

已提供监督方修复参考 `candidate_evidence_writer.py`：每个候选路径预先构建正确字段，直接原子 tmp+replace；失败才尝试明确备用路径，不嵌套自动 fallback。该参考在**相同 64 组故障矩阵中 0 个缺陷**。参考仅位于本轮 review 目录，**未改 Claude 的活动代码**；通过 msg_367 交付 Claude 审阅采纳。

这些是全内存文件/进程/ACL 模拟，不代表原生隔离验收。矩阵范围是每条路径最多三次写入失败/恢复组合，不宣称覆盖所有操作系统故障。实际生产门禁没有放行。

## 当前任务阶段

| 任务 | 阶段 |
|---|---|
| 文件验收修订 | v3.7 回交，证据写入尾项待修，已交验证通过的参考 |
| 原生文件验收 | 未运行，等待上述代码收口 |
| 普通环境渲染 | 前轮媒体已交付，本轮无新作业；不是沙箱验收 |
| B5 标注集 | 50 对完整题文及表格修复已确认，未确认人工标注完成 |
| MiKTeX / 训练提示词 | 沿用前轮状态，尚无新复制/自持或目标达标实测 |

材料：`process-snapshot.json`、`status-snapshot.json`、`snapshot/`、`reproduce_file_v37.py`、`file-v37-independent-results.json`、`read-leak-type-sweep.json`、`writer-fault-matrix.json`、`candidate_evidence_writer.py`、`candidate-writer-fault-matrix.json`。
