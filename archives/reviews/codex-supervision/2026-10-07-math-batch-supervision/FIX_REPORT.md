# Claude Code 数学批审与发布链监管修复

本轮独立检查 Claude 提交的 batch1–3 共 38 道训练题及新批审工具。38 题的主要计算结果成立；发现 5 条条件或答案完整性需要补严、7 条场景需要精确化或补全论证，去重后共 10 条修订。修订已形成新候选，保留原始题目、旧批次回执和上一轮 30 条修订。

## 已执行修复

tools/math_review_batch.py 原版有四类可复现缺陷：空规格和重复题号仍能打包；bundle 未核验实际源文件和记录版本；已有目录可被覆盖；重跑时旧 receipt 被写入新清单，形成错误的自包含绑定。复现保存在 original-defect-reproductions.json。

最终契约为 math-review-batch-receipt-v3。冻结核心 manifest 使用具名 SHA 和字节数固定，761 条范围和身份唯一性重新核验。extract 和 bundle 均逐条核验源文件 SHA、源行号、记录身份和规范 JSON SHA。批次规格非空、题号唯一、禁止夹入前轮已修订题号；作者裁定必须有具名理由，已有绑定不允许被工具静默替换。

每个新批次保存六项：批次报告、绑定裁定、原规格快照、原裁定快照、输入绑定、打包源码快照。receipt 自身不列入清单。verify 逐项核验哈希并重新构建行、统计、源绑定和源码快照绑定。输出必须在项目 reviews 下的新目录；旧目录、核心冻结包和前轮交付目录受保护。异常返回非零。工具打包成功只证明版本与发布链成立，不签署数学、同核心隔离或准入通过。

batch1–9 的 217 条作者裁定已重新绑定至 rebound-v3/，保留全部 v1/v2 原件。batch4–9 的 179 条作者数学结论仍待本模型逐题独立审阅，重新打包不代表数学通过。batch9 邮件及提交标题写 v2，实际 receipt 已是 v3；本轮以原件真实 schema 为准，保留旧描述并在新回执中更正。

## 38 题的独立结果与 10 条修订

- calc-green-005、calc-area-009：明确半径参数 a>0，使正向圆周和标准摆线一拱的几何条件完整。
- linalg-064：补齐全部非零特征向量 t(1,0)^T、t(1,-1)^T（t≠0），与对应一维特征空间区分。
- prob-040：把有限 n 的笼统“很大、很小、近似”改为 p_n∈[0,1]、np_n→λ 的严格质量极限。固定 k，利用对数夹逼证明；λ=0 用 Markov 界单列。场景使用离散概率质量点，p_n=5/n、方差 5−25/n，替换小数，不以有限柱图验证极限。
- prob-041：明确 σ>0，给出密度缩放和精确峰高。原场景中的正态区间近似数值改为 erf(1/√2)、erf(√2)；原任务仍为密度参数影响，没有增加题目。
- calc-limit-006：初始角精确取 π/4；展示 sin x<x<tan x 的面积包含、夹逼和偶性，不用“约45度”或有限图形代替极限证明。
- linalg-053：用列向量叉积、底面积 √14、高 10/√14 和体积 10 替代动态测量所得数值证明。
- linalg-054：原方程固定显示；另设明确区分的 D=0 示例，分别覆盖平行不重合无解、重合无穷解。
- linalg-067：以 A^TA=I 推出任意向量内积和距离保持，动态图形只作示意。
- geom-028：场景补上一次项系数推出 n=0；仅由 l=m=0 不能得出直线退化。

详细逐题绑定在 independent-review-38.jsonl；38 项精确计算佐证及定理条件说明在 exact-math-witnesses-38.json。实际完成 61 条精确恒等式核验，并使用符号积分、精确有理数、矩阵运算与明确的定理推理，没有数值近似。符号计算是具名计算的佐证，不冒充通用自动证明。

## 候选、验证和范围

corrections-10.jsonl 保存完整 before/after 字段、源绑定和修订记录。candidate-sources/ 包含六个完整源文件，共 497 条活动范围记录：以上一轮 admission-v2 为父版本，额外修改 10 条，上一轮 30 条修订的最终记录 SHA 全部保持；其他行字节保持。没有修改现役数据、锁文件或冻结包。

verify_candidate.py 独立重新核验原始源、父版本清单、候选源、明确变更、未变更行、30 条继承修订及 38 条审阅/计算佐证绑定。实际执行通过。原 batch1–3 的源版本和回执 SHA/计数也已逐项核对。

45 项针对性回归及 3 个子测试通过，覆盖空/重复规格、假身份、源版本漂移、缺少理由、路径越界、旧目录保护、重新哈希后的内部假统计/假绑定/假准入/源码漂移、错误退出，以及 runpy 参数与退出语义。上轮八个已测工具/测试的源码 SHA 保持一致，无需重复声称已重新运行上轮 90 项。

观察器 20432 正常 STOP；新隐藏 worker 12952 已确认心跳。监听增加新批审工具、测试、规格和全部批审材料目录。后台观察器只记录，不自动执行模型审阅或准入。

本轮结论只覆盖具名候选的 38 道数学审阅和发布链修复。同核心训练/评测隔离、剩余数学批次和新候选渲染仍未完成，active_data_admission=PENDING，production=CLOSED；没有签发 PASS_CORE_SCOPE，也没有开展延期的原生、模型或双端外部实验。

## 复验入口

- 工具：python tools/runpy.py tools/math_review_batch.py bundle --batch <批次> --out reviews/<新的批次目录>
- 包绑定：python tools/runpy.py tools/math_review_batch.py verify --input reviews/<新的批次目录>
- 10 条新增候选：python reviews/codex-supervision/2026-10-07-math-batch-supervision/verify_candidate.py
- 精确佐证：python reviews/codex-supervision/2026-10-07-math-batch-supervision/verify_exact_38.py（会重新生成本目录的计算结果文件；交付冻结后建议在副本运行）

源码与交付的具名 SHA 见 tested-source-bindings.json 和 delivery-manifest.json。原始历史语料、旧审核回执和旧版本继续保留。
