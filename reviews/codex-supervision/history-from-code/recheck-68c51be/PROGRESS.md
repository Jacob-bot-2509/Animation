# 当前任务进度

更新日期：2026-10-03。**协作角色：Claude Code 同时承担统筹(copilot 职责)与执行职责;
Codex 独立复审(用户指示监管)。** 未训练;三款模型已下载(用户批准 2026-10-03,
筛选完成,baseline=Qwen3-4B 已拍板);依赖栈已装(审查快照
reviews/2026-10-03-pretrain-review/dependency-inventory.json)。

## 当前阶段

- **底座模型筛选完成(2026-10-03):baseline = Qwen3-4B(用户拍板)**;
  三方对照证据见 reviews/2026-10-03-model-screening/,临时实验组已按计划撤走;
  落选模型(2.5-7B/3-8B)保留在 .models/ 作对照。
- 训练任务继续挂起:等 eval/test 独立制作与冻结、preflight 八项门禁、用户训练批准。
- **eval/test 审阅稿已出(2026-10-03,用户指示由我方起草)**:
  dataset-eval.md 100 题(同题多解+思路展开:数学分析 30/解析几何 20/概率论 15/高等代数 35),
  data-test.md 150 题(泛化综合:分析 45/几何 25/概率 25/代数 40/跨学科 15);
  全部确切值、计算题与证明题兼备、无过程省略;与 train 63 条题目族不同、ID 前缀 eval-*/test-*。
  渲染 PDF 供用户审阅:outputs/review/{dataset-eval,data-test}.pdf(公式零残留,已验证);
  渲染工具 tools/render_review.py + tools/assets/mathjax-tex-svg.js(本地渲染器)。
  状态:待用户审阅题目与解答;定稿后再转正式 markdown→JSON→JSONL(契约见 EVAL_TEST_PREP.md §3.5)。
- **数学复查一轮已整改(2026-10-03)**:Codex 逐题复查报告已迁移至
  reviews/2026-10-03-math-review/review-math.md(250 题全查,A/B/C 分级)。
  A 级 5 项、B/C 级 55 项全部按报告修复(精确值、反函数、直纹族、反射轴、
  部分和奇偶子列、分部积分第二解析解、草稿残留清除等);全局排版两类问题
  (矩阵列分隔符 & 被误转义、\lt/\gt 连写)在渲染器中修复;PDF 已重渲染
  (公式 4903 条零残留、无 LaTeX 泄漏)。
- **eval/test JSON+JSONL 已生成(2026-10-03,用户指示,harness 预跑)**:
  data/v1/eval/dataset_eval.{json,jsonl} = 300 行(100 题×3 解法,
  problem_id/solution_id/method 复合身份,GS3 同题同题干/method 唯一已自检);
  data/v1/test/dataset_test.{json,jsonl} = 150 行(id 全局唯一)。
  入场检查:problems=0,quarantine=450(仅"可选元数据缺/空"一项,
  function_family/visual_style/efficiency_tags 待补→candidate 语义);
  eval_test_prep check 通过:与 train 精确重叠/近重复隔离 OK。
  scene_spec 由已复查动画要点按模板展开(candidate,后续精修);
  source=self-authored,license=Internal-Research-Use-Only;
  涉及知识点/思路展开保留在 md(契约无对应字段)。
  报告:reports/2026-10-03-eval-test-intake.md。

- 数据：63 条自撰候选数据(数学分析 19 / 概率论 9 / 解析几何 12 / 高等代数 23),
  dataset.md / JSON 数组 / data/v1/raw/*.jsonl 三处一致,入场检查 clean;
  审计记录级 hard=0,63 条全部 **candidate**(code/render_status 缺失,不假绿)。
- 训练前准备就绪：manifest-train(provisional,63 条 split=train 用户拍板)、
  train_config.template(TBD 契约)、backend 适配器契约(仍是注册表占位)、
  BASE_MODEL_SHORTLIST(baseline=Qwen3-4B 已拍板)、
  eval/test 已生成已冻结(300/150 条,锁 data/{eval,test}-v1.lock.json)。
- preflight --ready 实测 **NOT READY**(model_dir/run_snapshot/near_dup_calibrated/
  freeze_gate/asset_evidence 阻断),fail-closed 生效。

## 审查台账状态

| 项 | 状态 |
|---|---|
| A1-A8 数据与入场可信度 | 全部关闭(JSONL 口径、近重复实现、入场边界、A4/A5 语义、A6 类型/别名、A7 冻结写保护、A8 防泄漏哈希) |
| B1 运行快照 | GS4 反例已修(dirty 内容哈希绑定、config fail-closed、CLI verify);待 Codex 独立复验 |
| B2 严格 preflight | GS2 反例已修(逐条资产证据 + 8 项核心门禁);待 Codex 独立复验 |
| B3 冻结评测与指标 | 空锁/覆盖/绑定已过;固定指标、逐样本结果与失败分类待 eval/test 冻结后验收 |
| B4 执行隔离 | GS5 反例已修;memory(job object)+ network(socket shim 封堵 connect/connect_ex/sendto/getaddrinfo+死代理,OS 级边界如实标注)已实施;exec_isolation 门禁 PASS(2026-10-03);待 Codex 独立复验 |
| B5 阈值校准 | UNCALIBRATED 传播并阻断;分语言/长度校准待真实标注数据(用户侧) |
| B6 产物写入 | GS1 反例已修(碰撞拒绝/阶段持久化/清理失败不回滚/恢复冻结保护);待独立复验 |
| B7 类型契约 | 已关闭(分类/来源/正文/答案/场景元素/可选元数据类型) |
| C1-C12 | 延期清理,主线收尾集中处理 |

## 最新验证

- **354 passed + 29 subtests**(2026-10-03,全量);eval/test 入场 clean
  (450 条 problems=0/quarantine=0);data_check 主清单 6 条目通过;
  eval/test 双锁 check 通过;train/eval/test 隔离通过(近重复最大 0.6667<0.7,
  阈值仍 UNCALIBRATED);harness 预跑终版
  dataset_audit_2026-10-03-eval-test-r7(hard=0)。
- manifest: data/v1/manifest.json(6 条目:63 条 split=train+eval+test);
  data/v1/manifest-train.json(provisional train,4 条目 split=train,用户拍板)。

## 下一步顺序(统筹视角)

代码侧可继续推进(不需用户批准)：
1. **B4 完整执行隔离**(fs/network/memory)与不可信数学输入保护;
2. **B1 快照补全**(训练配置参数入快照、完整重放);
3. C 类清理(C2 空 split 误报、C5 配置示例、C12 效率整理)。

需要用户批准/提供的门：
1. ~~eval/test 样本制作~~(已完成:100/150 题,300/150 条,已冻结);
2. ~~模型下载~~(已完成,Qwen3-4B baseline 已拍板;量化方案 4bit NF4+BF16 候选待正式训练批准);
3. B5 校准的真实标注数据(阈值 0.7 仍 UNCALIBRATED);
4. 训练超参数(seq=1024 候选,审查报告 §建议;lr/epochs/LoRA 参数待定);
5. 正式训练批准(训练后端仍是占位注册表,未实现)。

完整规划见 [PIPELINE_PLAN](PIPELINE_PLAN.md)、[训练前准备](TRAIN_PREP_PLAN.md)、
[eval/test 接口](EVAL_TEST_PREP.md)、[审查备忘录](REVIEW_BACKLOG.md)。
