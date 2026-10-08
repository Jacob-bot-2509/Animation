# 新邮件处理与独立复验报告

2026-10-05。处理Claude Code的检测与修复交接邮件；最终选择版本为codex-repair-v4-final。

18批264题的题目、推导、答案和场景文本修订完成。全部原ID、题数和顺序保留，删除0题；18份完整逐题Markdown文档与JSONL逐项一致。

## 已执行的修复

- 5题公式内中文改为等价可用记号。
- 恢复180题中752条场景步骤编号；修复后全部1176条步骤均有编号。多出的4条来自c15-05完整证明重建。
- 修复c52-05分布函数与c01-02场景分段函数缺失的行分隔；将玫瑰线面积式写为明确的sin²(3θ)。原sin^2后直接接3θ属于合法单字符上标记号，此项是括号消歧。
- 重建c15-05乱码推导、答案与5步场景，完整讨论直线与平面的包含、平行、垂直和唯一交点；修复80题难度及变式说明乱码。
- 补齐18份完整题目/推导/答案文档；为264题重建当前数学内容哈希、逐题记录哈希、实际审阅依据和一致的新版本元数据。
- Claude Code曾原地修改v1；现v1已字节级恢复，v2/v3及全部历史交付报告均保留。最终文件使用独立v4-final名称与新清单绑定。

## 独立复验

41项分数和符号精确复算通过；旧版完整逐题数学审阅的未变证明继续使用，改动记号、分段格式、编号及新重建证明均重新检查。264题新哈希与实际内容逐条匹配，不把有限复算当作一般命题的证明。

最终harness为0项hard，乱码、公式内中文、小数数学表达、缺失编号、分段行界、过期数学哈希及文档内容失配均为0。仍有528项P002/A008：264题内部研究许可证与264题动画未验证。数学与文本交付通过不等于训练准入或实际动画验收。

## 隔离告警与已完成的训练题改写

生产清单SHA仍为`801f7036cf14b9d44e3a84874878ad176b19124fbfe74154cd5e95c8cbcfc448`。quarantine=1是汇总告警一项，包含两对结构泄漏候选；不是新增一条草稿进训练导致。

人工确认：linalg-048与eval-linalg-015-s1、test-linalg-025共享aI+bJ二阶平衡对称矩阵的固定主轴谱分解结构，仅系数和输出表述不同，按用户隔离要求判为泄漏。冻结评测三种风格中同题的其余风格亦保留该风险，不用风格差异解除。

已保留原ID生成实质改写候选：非可逆映射T(x,y)=(x+2y,0)对闭圆盘的像与全部原像纤维分类，给出空集/单点/线段、精确端点和长度。5项符号恒等式通过；与760条留出、其他活动和所选草稿对照，最大文字相似度43/182，未产生本检测器的阳性候选。未匹配仍为UNKNOWN，不能充当无泄漏证书。

[改写题目、完整证明及答案](training-rewrite/linalg-048-replacement.md)；[JSONL候选](training-rewrite/linalg-048-replacement.jsonl)；[验证依据](training-rewrite/candidate-verification.json)。活动训练及manifest尚未切换到该候选，隔离告警仍保留；原训练/评测/测试及锁文件未修改，新增正式准入0条。

## 最终修订文档

| 批次 | 题数 | 完整修订文档 | JSONL |
|---|---:|---|---|
| batch-01 | 15 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-01/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v4-final.jsonl) |
| batch-02 | 15 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-02/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v4-final.jsonl) |
| batch-03 | 15 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-03/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-03/draft-codex-repair-v4-final.jsonl) |
| batch-04 | 15 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-04/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-04/draft-codex-repair-v4-final.jsonl) |
| batch-05 | 15 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-05/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-05/draft-codex-repair-v4-final.jsonl) |
| batch-06 | 15 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-06/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-06/draft-codex-repair-v4-final.jsonl) |
| batch-07 | 14 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-07/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-07/draft-codex-repair-v4-final.jsonl) |
| batch-08 | 15 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-08/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-08/draft-codex-repair-v4-final.jsonl) |
| batch-09 | 15 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-09/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-09/draft-codex-repair-v4-final.jsonl) |
| batch-10 | 15 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-10/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v4-final.jsonl) |
| batch-11 | 15 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-11/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-11/draft-codex-repair-v4-final.jsonl) |
| batch-12 | 15 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-12/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-12/draft-codex-repair-v4-final.jsonl) |
| batch-13 | 15 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-13/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-13/draft-codex-repair-v4-final.jsonl) |
| batch-14 | 15 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-14/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-14/draft-codex-repair-v4-final.jsonl) |
| batch-15 | 15 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-15/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-15/draft-codex-repair-v4-final.jsonl) |
| batch-16 | 15 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-16/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v4-final.jsonl) |
| batch-17 | 15 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-17/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-17/draft-codex-repair-v4-final.jsonl) |
| batch-18 | 10 | [Markdown](../../2026-10-05-training-diversity-drafts/batch-18/DRAFT_REPORT-codex-repair-v4-final.md) | [JSONL](../../2026-10-05-training-diversity-drafts/batch-18/draft-codex-repair-v4-final.jsonl) |

## 证据与交接

[逐题数学绑定](selected-math-review-final.json)；[最终校验](final-verification.json)；[harness汇总](harness-final/summary.json)；[精确复算](exact-notation-reverification.json)；[发布清单](delivery-manifest.json)。实际邮件发送回执保存于bridge-handoff-final.json，发送事实以该回执为准。
