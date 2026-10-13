# 第09–18批精确数学修订报告

2026-10-05。用户授权由Codex全权审校并执行修改，修订文件交给Claude Code跟进。

完成145题；全部保留原ID、题数及顺序，删除0题。80题改写题目结构或补全题干，103题修改至少一个数学字段，42题原数学内容保留。全部145题的场景文本与最终题干、证明和答案重新绑定。

## 修订内容

- 删除小数答案和未经证明的近似误差，使用分数、根式、有限和、指数、Φ及Φ逆函数。有限概率与极限概率分别表述。
- 修正零分母直线式、剪切边方向、线面包含关系、平面束遗漏成员、曲面正则性与退化、交线端点及参数域。
- 补齐数域、系统相容性、多项式环单位、Jordan链、辛形式配对和随机事件独立性。柯西反例只证明删去假设后不能普遍保证结论。
- 重复题保留原ID，改成实质不同的约束或任务；同核心只换数值的题按泄漏或重复处理，历史父题与风险溯源保留。

## 独立复验

165项符号或有限精确复算通过，精度与编码扫描零问题。概率有限和另用整数卷积、Eulerian递推等方法核验；一般收敛、正则性和极限定理依据逐题人工证明，有限检查不充当通用证明。

145×450=65250次冻结评测与测试方法记录对照，另对前八批、47条活动训练和当前批次作34510次两两对照。最终5条留出候选（3个不同题对）及1条草稿/活动候选均有具体人工裁决，未保留本次识别出的同核心数值变体。未校准检测器的阴性或UNKNOWN不等于无泄漏证书。

## 各批修订文件

| 批次 | 题数 | 新题库 | 题目、推导、答案文档 |
|---|---:|---|---|
| batch-09 | 15 | [JSONL](../../2026-10-05-training-diversity-drafts/batch-09/draft-codex-repair-v1.jsonl) | [Markdown](../../2026-10-05-training-diversity-drafts/batch-09/DRAFT_REPORT-codex-repair-v1.md) |
| batch-10 | 15 | [JSONL](../../2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v1.jsonl) | [Markdown](../../2026-10-05-training-diversity-drafts/batch-10/DRAFT_REPORT-codex-repair-v1.md) |
| batch-11 | 15 | [JSONL](../../2026-10-05-training-diversity-drafts/batch-11/draft-codex-repair-v1.jsonl) | [Markdown](../../2026-10-05-training-diversity-drafts/batch-11/DRAFT_REPORT-codex-repair-v1.md) |
| batch-12 | 15 | [JSONL](../../2026-10-05-training-diversity-drafts/batch-12/draft-codex-repair-v1.jsonl) | [Markdown](../../2026-10-05-training-diversity-drafts/batch-12/DRAFT_REPORT-codex-repair-v1.md) |
| batch-13 | 15 | [JSONL](../../2026-10-05-training-diversity-drafts/batch-13/draft-codex-repair-v1.jsonl) | [Markdown](../../2026-10-05-training-diversity-drafts/batch-13/DRAFT_REPORT-codex-repair-v1.md) |
| batch-14 | 15 | [JSONL](../../2026-10-05-training-diversity-drafts/batch-14/draft-codex-repair-v1.jsonl) | [Markdown](../../2026-10-05-training-diversity-drafts/batch-14/DRAFT_REPORT-codex-repair-v1.md) |
| batch-15 | 15 | [JSONL](../../2026-10-05-training-diversity-drafts/batch-15/draft-codex-repair-v1.jsonl) | [Markdown](../../2026-10-05-training-diversity-drafts/batch-15/DRAFT_REPORT-codex-repair-v1.md) |
| batch-16 | 15 | [JSONL](../../2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v1.jsonl) | [Markdown](../../2026-10-05-training-diversity-drafts/batch-16/DRAFT_REPORT-codex-repair-v1.md) |
| batch-17 | 15 | [JSONL](../../2026-10-05-training-diversity-drafts/batch-17/draft-codex-repair-v1.jsonl) | [Markdown](../../2026-10-05-training-diversity-drafts/batch-17/DRAFT_REPORT-codex-repair-v1.md) |
| batch-18 | 10 | [JSONL](../../2026-10-05-training-diversity-drafts/batch-18/draft-codex-repair-v1.jsonl) | [Markdown](../../2026-10-05-training-diversity-drafts/batch-18/DRAFT_REPORT-codex-repair-v1.md) |

## 版本与边界

draft-selection.json已保留前八批选择对象并追加十批，18批合计264题数学复核完成。实际账本读取264条；新增正式准入0条。现有训练、评测、测试、manifest及锁文件未改动；原始草稿、前八批交付和旧审校证据的保护哈希均保持。

本次不启动训练，不生成准入证书；动画只复核文本，未进行渲染验收。正式准入证据须绑定这18批新文件的实际哈希，不能沿用旧版本结论。

逐题依据：[per-question-review.json](per-question-review.json)；独立数学检查：[exact-reverification.json](exact-reverification.json)；结构裁决：[structural-review.json](structural-review.json)；发布哈希：[delivery-manifest.json](delivery-manifest.json)。交接消息及实际发送回执另存bridge-handoff.json，以回执为发送事实。
