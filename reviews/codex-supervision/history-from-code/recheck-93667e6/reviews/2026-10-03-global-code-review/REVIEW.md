# 整体代码审查（2026-10-03）

基线：db8f63b；源码 SHA256 与完整反例结果见 [results.json](results.json)。
结论：基础设施回归通过，但入口间的契约尚未闭合。新确认三类 P1 正确性问题，需在正式数据划分/验收前修复；小范围类型与维护问题按阶段处理。没有发现本轮真实数据被覆盖或真实评测污染的证据。

## 优先发现

### G2 / A7 / P1：新入场工具能绕过冻结写保护

位置：src/animtrain/dataset_intake.py:85，tools/dataset_intake.py:102，src/animtrain/fs_guard.py:16。
convert 与 report 只检查输出是否存在，force=True 时不查询冻结锁或冻结路径。

独立反例在三个互不干扰的临时目录中各创建有效 eval.lock.json：
- convert_array_to_jsonl(src, frozen_eval, force=True) 成功并修改冻结数据。
- report --out frozen_eval --force 返回 0 并以 Markdown 覆盖冻结 JSONL。
- report --out eval.lock.json --force 返回 0 并覆盖锁本身。

事后 check_frozen 发现变化，不能代替写入前拒绝。split 的现有保护并未覆盖新入口。
修正方向：统一写前守卫，保护冻结文件与锁本身；发现坏锁应拒绝写入，force 不得绕过。保留明确的跨目录锁接口，覆盖 CLI 和核心调用。
这是已有 B6/BR5 在新入口上的缺口，原 split 反例通过不代表所有写入口通过。

### G1 / A6 / P1：manifest/data_check 与入场契约不一致

位置：src/animtrain/validate.py:177、210、229；tools/preflight.py:66；src/animtrain/fields.py:46。

同一份合成输入在 intake 被拒绝，但 validate_manifest 可 ok=true、data_check CLI 返回 0：
- 把任意 .txt 登记为 train：代码只拒绝 .json，没有使用 .jsonl 允许列表。
- 单个空 train JSONL：没有样本行仍通过；check_fields CLI 也报告缺失 0 行并返回 0。
- 仅有 id、缺 problem/solution/answer 的行：字段检查失败，但 manifest 没消费字段门禁。
- 同文件重复 ID，或同一 train split 下两个文件 ID 冲突：集合运算去重后无错误；完整入场契约明确要求全局唯一。

preflight 的 data_manifest 项仅消费 validate_manifest，未接字段/入场检查或与数据哈希绑定的相应证据。
修正方向：按选定任务契约统一样本验证，至少落实 JSONL 允许列表、非空数据、全局 ID 唯一、所选 schema 必需字段。raw 辅助元数据与正式样本用途仍须区分，不能把所有 raw 文档套成动画样本。
A1/A3 的原反例保持已修；新增跨入口反例由 A6 跟进，不能宣称整体已经统一。

### G3 / A8 / P1：防泄漏比较整行 JSON，元数据能掩盖完全相同的任务正文

位置：src/animtrain/manifest.py:95，src/animtrain/validate.py:40、256、261。
精确哈希是整行文本；近重复 shingle 也直接吃整行 JSON。与近重复阈值是否校准是两个独立问题。

合成 train/eval 的 problem、solution、answer、scene_spec 完全相同，仅 id 与 function_family 不同（固定随机种子的合法长字符串）：
- intake clean。
- 整行 Jaccard 约 **0.04744**，低于默认 0.7。
- validate_manifest ok=true、exit_code=0，精确和近重复均漏检。

不能依赖换阈值来保证同题识别。应定义题目/核心正文的规范化表示，元数据不参与防泄漏相似度；同题多解也应留在同一集合。独立测试至少覆盖换 ID、改元数据、不同序列化、同题不同解。
当前真实数据仍处 raw，未执行正式划分，本反例不等于当前真实集合已经污染。

## 随阶段补齐

### G4 / B7 / P2：字段与场景元素类型约束不完整

位置：src/animtrain/dataset_intake.py:103、130。
当前 check_record 接受 objects=[]/steps=[]、objects=[null]/steps=[false]；category/source 非空容器及错误元数据类型也可无问题。
现有契约只明确要求“两列表”，没有完整规定元素类型、长度等，不能把所有类型细节当成既有明确规则。

请在选定 schema 中明确：分类/来源文本、风格/函数族文本、标签列表，以及场景对象/步骤非空文本列表的范围，并让检查与文档一致。正式动画生成前完成；不为未来任意任务提前扩展所有格式。

## 已知主线限制复核

- B2：核心 run_preflight 在只有 GPU/model/data_manifest/run_snapshot 的合成成功结果时仍可 ready=true；CLI 固定 MathTex 与 Eq(2+2,4) 不能替代当前资产验收。已有缺口仍未关闭。
- B4：不可信渲染默认拒绝，这是有效保护；trusted=True 仍无完整文件系统/网络/内存隔离。math_check 的 sympify 字符串和黑名单不是完整不可信输入边界。本轮没有执行恶意表达式。
- B5：validate_manifest 总是 near_dup_calibrated=False，CLI READY 会被它阻断；实际校准证据仍未接入。
- B1：快照的 manifest 哈希与 seed/dirty 框架保留；完整配置重放、代码状态与指标契约仍待验收。
- B3/B6：split 冻结保护现有路径保留；多文件写入不是事务，锁的坏字段可抛异常（C9）。没有因这些已知限制重复扩展本轮修补。

## 低影响备忘录

- C1 的“重复 _load_sample_ids 定义”已不适用于当前源码（现在仅一个定义）；剩余旧变量、重复读文件/过时注释可随模块修改清理。
- C4 已部分处理：非零正式数据 size 不一致会拒绝；raw/size=0 仍未全面约束，当前依赖 SHA256 完整性。
- C10：manifest/记录的异常类型、目录当输入、非 UTF-8 等路径可能抛回溯；先作为可定位错误与 CLI 异常处理的一致性整理，出现错误放行或覆盖立即升级。
- C11：工作区 pyproject 为 0.1.0，包 __version__ 与 README 为 0.2.0；NEWRELEASE.md 被外部删除但 README 链接仍在。没有覆盖这些已有外部变更，下一次发布前统一。
- C12：校准函数重复计算相似度、preflight 参数缺失检查位于固定渲染之后、GPU 子进程缺超时等效率/诊断整理，主线收尾处理。

## 审查范围与证据

已阅读 src/animtrain 正式模块、tools 正式 CLI、主要回归测试及 PIPELINE_PLAN/NEXT_CYCLE_PLAN/DATASET_SCHEMA；检查数据/字段/静态代码、渲染/数学、快照、冻结、扫描、划分与预检的连接。
外部未跟踪 tools/dataset_audit.py 及审计产物未执行或修改；未下载/安装、训练或发布。
- 全量：**186 passed + 29 subtests passed**，6.35 秒。
- [独立反例脚本](probe.py)：只读当前真实数据；覆盖实验全部位于自动清理的临时合成目录。
- 当前 63 条入场 clean、真实 manifest 通过；全部真实 JSONL 输入哈希及正式源码哈希在探针前后不变。
- 本轮只新增审查报告/探针并更新 REVIEW_BACKLOG；不改源码、不提交 Git、不修改真实数据。
- 已发 Claude Code msg_1790962156456_174、msg_1790962260001_175，主力负责实质修复。
