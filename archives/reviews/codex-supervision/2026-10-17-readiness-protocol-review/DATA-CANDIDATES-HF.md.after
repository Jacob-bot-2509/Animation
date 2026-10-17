# 外部候选数据与用途登记（2026-10-17 审订）

当前是来源与设计登记，不是已下载、已审查、已获资格或已导入的数据。Claude 邮件 852 报告其侧用户选择了 NuminaMath 上限 2000 条、首批目标 300 条及外测方案；在本页保留该来源与额度，不把邮件扩成 Codex 自动下载、模型改配或开训授权。用户在当前 Codex 会话亲自确认的有限隔离政策继续有效。

静态来源登记、数学审查、隔离筛查与候选构建可以在训练 READY 前完成；执行不可信生成代码须先通过相应执行隔离门禁。具体格式、分工与依赖见 [准备证据与接线协议](READINESS-EVIDENCE-PROTOCOL.md)。

## 来源与互斥用途

| 来源 | 核验到的信息 | 本方案用途及限制 |
|---|---|---|
| [AI-MO/NuminaMath-CoT 官方卡片](https://huggingface.co/datasets/AI-MO/NuminaMath-CoT/blob/main/README.md) | 标注 Apache-2.0；字段含 source/problem/solution/messages；来源包含中国中学题及竞赛题，处理链含译成英文 | 候选训练题源；不能把 cn_k12 来源标记当作现成中文子集。实际语言、数学正确性、原始来源与许可按所选记录核验。总量不超过 2000；首批 300 是目标，不以凑数替代质量 |
| [TIGER-Lab/TheoremQA 官方卡片](https://huggingface.co/datasets/TIGER-Lab/TheoremQA/blob/main/README.md) | MIT；800 条 test；Question/Answer/Answer_type/Picture；无逐步 solution 字段 | 依邮件中的外测安排，当前登记为 EXTERNAL_QA_ONLY。整集题文、答案及其生成解答都不得进入训练、提示示例或选优反馈。移除旧版同时列作训练题源的冲突 |
| [UGMathBench 官方卡片](https://huggingface.co/datasets/UGMathBench/ugmathbench/blob/main/README.md) | GPL-3.0；5062 个基础问题，每题 3 个随机版本，16 学科/111 主题 | EXTERNAL_QA_ONLY。完整版本实例数应核对为 5062×3=15186，不能声称它们是 15186 个独立核心题。实际缺失、损坏和排除另列 |
| ManiBench | 本轮未收到唯一官方 URL、版本、许可原件和固定样例清单 | 仅记 CANDIDATE_ACCEPTANCE_REFERENCE，不能直接计入验收或导入训练 |
| manim_animations_10k、bespoke-manim、adaption-unified-manim-instructions、NL2MANIM | 本轮未收到逐来源的唯一仓库标识、固定 revision 与许可原件 | 仅保留研究候选；许可不明的代码、题文、视频、推理轨迹及其改写不进训练。研究抽象风格原则不等于获得复制或改编具体材料的许可 |

NuminaMath 卡片的来源统计与文件统计不能替代固定 revision 的实际清点。不得根据“约 86 万”预填导入记录数。

GPL-3.0 来源由[仓库许可证原文](https://github.com/YangLabHKUST/UGMathBench/blob/main/LICENSE)核对。这里的“仅外测”是项目数据用途约束，不代表免除许可义务，也不能仅凭 GPL 标签断言模型权重必然受何种许可约束。原始数据与官方评测代码的许可、版权声明、修改和分发行为分别登记；不自动复制其代码进项目。此前“传染性”与“学习风格无需许可”的笼统判断已撤除。

## 任务边界

本项目训练任务是 problem + solution → scene_spec。TheoremQA/UGMathBench 的短答案外测考察答案正确性：只将题目及必需图片给模型，参考答案仅供判分端使用；不把参考答案放入模型提示。不生成逐步解答用于训练，也不把“没有逐步解答”误写成模型不需要产出答案。

该外测不直接测量 scene_spec 的 R/E/M/F，更不能把短答案正确率当动画数学正确率或画面忠实度。当前模型的 QA 输出适配、图片输入能力、输出解析和答案类型判定尚待实现与核验；本轮没有跑外测。只支持文本时，含图题不得悄悄丢图继续算完整 800 条，须另报适用范围。

同一来源及其翻译、改写、数值版本按核心族一起分配用途。TheoremQA 本方案不再承担补充高等数学训练深度的角色；训练来源不足如实报告，不调用冻结外测答案补齐。

## 候选导入与外测登记

先固定来源 revision、许可与实际文件 SHA，再进行学科/难度分层抽样、独立数学核验及当前 train/eval/test/外测/holdout 全部适用集合的泄漏核对。以语义核心判断为准；低文字相似度、签名不同、换数值均不能自动认定隔离。已知同核心冲突不因有限隔离政策而忽略。

上限不等于目标必须用满。每个阶段记实际计数与排除原因，保留原件和另版修订，不删除旧题来伪装通过。固定抽样方案及种子后再看结果，不根据外测反馈反复挑题。尚未查看的最终 holdout 只允许受限工具返回 ID/哈希/冲突判定，不能把题文送给调参会话。

外测模型、提示、判分器与规则先锁定后执行；如反复用于选模型或调参，应标为开发评测，不再宣称独立最终验证。外测数据、分数与训练语料分账，不在当前活动 manifest 或旧冻结锁中直接追加新来源。

本页只审订方向及矛盾，不宣称完成外部数据数学审查、许可全量核验、导入或训练准入。
