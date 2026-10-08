# 接手修复报告

已实际完成原输入恢复、场景暂存协议、九题数学新版本，以及发现的场景证明和公式错误修复。整体 264 题改写和独立验收尚未完成，正式发布、训练及资产准入未放行。

## 输入与发布链

原 20 个 chunks 和 listing 共 21 文件恢复历史原字节，SHA 全匹配；普通写打开已实测被可撤销 ReadOnly 拒绝。18 条原地改写完整另存，未丢失。未改 ACL、未终止 Claude 进程。Claude 的 msg560 已确认内部 Task 于 14:12 完成并停止写入。

新 inputs-v2 含 264 条完整记录及逐条来源绑定，均衡为 20 个非空只读分块。每个元素为 idx、record、binding；后续须读取完整 record，不能沿用旧九字段投影。

新增 tools/scene_sweep_protocol.py、tools/stage_scene_patches.py；split_scene_sweep.py 必须传入新 --out。新入口拒绝输出与输入/来源重叠、陈旧 SHA、重复 ID、数学三字段变动及读取期间漂移。验证与暂存共用快照。

旧 publish_row_patches.py 对任何包含 scene_spec 的补丁关闭自动切换 selector，包括混入未变答案字段或混合数学/场景批次的绕过。新入口只生成新文件及 draft-selection.candidate.json，关闭准入/渲染标志，不改活动选择器。39 项相关回归通过，真实 CLI 已产出三条小样版和 53 条合并版。

## 九题实际数学修订

math-corrected-v1 保存四科 47 条记录的新版本，其中修订 9 条；math-9-corrected.md 给出完整题目、过程、答案和场景步骤。修改已经落成文件，不再只是提案。

修订 calc-series-015/020、linalg-050/070、prob-038/039/042/043/046，纠正交错级数与余项界、Fourier 端点、秩零退化、有向面积、条件概率、有限有理估计量与 \(\pi\) 的区别、硬币公平性、标准化 CLT、半开可列分割。概率三题也补全题干条件和精确目标。

九题公式无 hard/quarantine，数学字段没有小数文字。32 项精确公式及具体证明缺陷检查通过；范围为具名公式与九题审阅，不表示其他 38 条或所有场景已经验收。原绑定训练文件及正式 manifest 未改；新版本未准入、未做动画验收。

## 场景结果与额外错误

workflow-run-result.json 原始字节已保全，SHA 为 92b4adf7c04659e8ae257ebaad687497bcda0187727b39fe2fe17159e5e5f1aa。身份/顺序覆盖独立重算为 264 条；作者报告 121 PASS、143 REVISE，返回 39 条修订。105 个后续智能体因余额不足失败是 Claude 的回报，作者工作流校验不等于 Codex 或视觉验收。

返回的“通过”结果仍有错误：draft-c36-01 把 \(y^{\mathsf T}AA^{-1}Ay\) 错误化成 \(y^{\mathsf T}Iy\)。已修成
\[
y^{\mathsf T}AA^{-1}Ay=y^{\mathsf T}IAy=y^{\mathsf T}Ay.
\]
对象、步骤及消去依据同步修改。精确反例 \(A=\begin{pmatrix}2&1\\1&2\end{pmatrix}\)、\(y=(1,0)^{\mathsf T}\) 给出 \(y^{\mathsf T}Ay=2\)、\(y^{\mathsf T}Iy=1\)，确认旧中间等式错误。

三类小样修正保留：Gram 逐项行列乘法、收敛几何上界与可积性、贝叶斯公式移除中文及条件独立性用途。嵌套分数也已加全括号。

39 条工作流结果与 18 条保全成果按 ID 合并，再由三条 Codex 修订覆盖对应目标，得到 53 条无重复候选。scene-candidates-53-v4 是实际新 264 条版本，其中 53 条场景改写；补丁为 scene-candidates-corrected-v4.json。53 条 scene 公式均无 hard/quarantine，未引入小数，题干/过程/答案与来源对应。

这仍是公式检查及具名重点数学复核，53 条完整独立数学/语义及视觉验收未完成。另有 90 条 REVISE 没有任何改写候选，ID 见 workflow-evidence-analysis.json；不将它们计为已修，也不将审计 264 计为改写全部完成。

## 核心分组与留出规范

core-families.corrected-v2.json 已交付至 reviews/2026-10-06-core-families。原绑定 47 条含 1 个双成员家族及 45 个单例，共 \(46\) 个核心任务；数学全量和密度验收另行记录。旧 pending 原字节保留。

holdout-design.corrected-v2.md 已交付至 reviews/2026-10-06-holdout-design。现有成员均已曝光，按未曝光成员排除规则合格总体为 \(0\)，不能从空总体抽样或宣称独立盲标。新规范明确辅助新总体、身份/别名/正文及曝光账本、分层权重、实际种子/算法、标注/裁决角色和开发/校准/最终验证隔离，并处理同题/同家族题对依赖。

每项单独的单侧置信水平 \(19/20\) 下，iid Bernoulli 的零误报/全检出解析基准为 \(299\) 个负例、\(59\) 个正例；真实分层有限总体需对应设计置信界。它们不构成新校准或两指标的联合置信证书。新未曝光总体和独立标注尚未建立，因此校准仍不能完成；没有伪造独立数据或标签。

## 当前状态

进度看板已同步实际产出。只读监听覆盖 174 条具名路径，worker PID 43628、launcher PID 42944；只记录，不自动审查或批准。

正式数据、18 个已选文件、eval/test 锁、旧原生回执及其 32 个来源绑定保持。协议 v3 两个新工具和回归文件未改。资产 \(1/497\) NOT READY、隔离 CLOSED、超参 PROPOSED；没有新原生渲染或模型训练。

最终字节/来源复验见 final-verification.json，实际测试输出见 suite-final.stderr.raw.txt，交付 SHA 见 delivery-manifest.json。入口使用见 OPERATING_GUIDE.md。剩余改写、全量数学/视觉验收、独立总体/校准均保留未完成状态，不宣称整项目完成。
