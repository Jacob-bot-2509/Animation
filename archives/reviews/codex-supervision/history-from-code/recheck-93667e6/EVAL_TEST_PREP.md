# eval/test 准备接口(EVAL_TEST_PREP)

> 2026-10-03,msg_197 初版;**2026-10-03 用户指示已生成** eval/test
> (data/v1/eval/、data/v1/test/,共 450 条),尚未冻结——已生成≠已冻结,
> 冻结需用户批准后经 freeze_data 执行。

## 1. 设计

- **eval = 同题多解**:对同一 problem 准备多种 solution(不同 method),
  评测模型在给定题目下生成 scene_spec/动画规划的稳定性与多样性。
  字段:problem_id(定位题目)/ solution_id(定位解法)/ method(解法命名)。
- **test = 综合泛化**:全新题目族,不与 train/eval 重叠,
  评测跨知识点泛化与场景规划质量。
- **隔离规则(与 train 严格隔离)**:
  - 题目族独立:test 题目不得来自 train 或 eval;
  - 近重复:5-gram Jaccard 阈值(当前 0.7 UNCALIBRATED,校准后启用);
  - 精确重叠与 ID 重叠零容忍(validate 的 A8 核心正文哈希 + ID 双重门禁)。

## 2. 目录骨架

```
data/v1/
  raw/       63 条 provisional train(现有,不动)
  eval/      dataset_eval.{json,jsonl}(300 行,100 题×3 解)+ manifest.json —— 已生成未冻结
  test/      dataset_test.{json,jsonl}(150 行)+ manifest.json —— 已生成未冻结
```

- eval/test 样本生成时必须写**新文件**,绝不覆盖 raw 或原始 JSON;
- 已生成(2026-10-03,用户指示);下一步:make_manifest 已完成(顶层与各目录),
  data_check → freeze(锁绑定 manifest,需用户批准)→ preflight --ready。

## 3. 验收脚本接口(tools/eval_test_prep.py,已实现只读部分)

- `status` — 报告 eval/test 是否已生成/已冻结(当前:均已生成、未冻结);
- `check <dir> [--train-dir]` — 已生成样本时:入场检查 + 与 train 的
  精确重叠(核心正文哈希)与近重复(5-gram Jaccard,阈值 0.7 UNCALIBRATED)隔离检查;
  若某目录确无样本,如实报告目录无样本(exit 0,不视为检查通过);
- `freeze <dir>` — **未授权:一律拒绝(exit 2)**;正式 freeze 在用户批准后
  经 freeze_data 执行。
- 报告契约:0 = 目录无样本(如实)或检查通过;1 = 硬伤(泄漏/坏样本);2 = 未授权。

## 3.5 JSONL schema(eval/test 样本契约)

eval(同题多解)单行:

```json
{"problem_id": "eval-p001", "solution_id": "eval-p001-s1", "method": "方法名",
 "category": "数学分析", "sub_category": "极限",
 "problem": "题干", "solution": "该解法的完整解答", "answer": "可判分终答",
 "scene_spec": {"objects": ["..."], "steps": ["..."]},
 "source": "待用户提供", "license": "Internal-Research-Use-Only"}
```

- 同一 problem_id 多条记录 = 同题多解,method 互不相同;
- test(综合泛化)单行:与 train/eval 相同的正式字段 + 全局唯一 id,
  题目族全新;
- 隔离检查对 problem 核心正文做哈希与 shingle,id/source/风格不参与(A8)。

## 4. 制作清单(下一步需用户提供)

| 项 | 内容 | 待用户决定 |
|---|---|---|
| eval 题目数 | 同题多解:每题 ≥2 个 method 解法 | 数量(建议 ≥20 题) |
| test 题目数 | 综合泛化:全新题目族 | 数量(建议 ≥20 题) |
| 来源 | 自撰或授权来源 | 逐题 source 与 license 证据 |
| 制作方式 | 用户自撰 / 授权后由我按 schema 起草 | 确认 |

## 5. 当前状态(如实)

- eval:已生成(300 行,100 题×3 解法,复合身份)、未冻结;harness 预跑
  dataset_audit_2026-10-03-eval-test-r2:hard=0,隔离通过(近重复最大 0.6667);
- test:已生成(150 行,id 唯一)、未冻结;
- 预跑剩余项:冻结锁(待用户批准)、可选元数据补齐(F010)、动画验证(A008)、
  许可证转正(P002),以及 manifest-train 的 raw/train 标签冲突(MF005/MF008,训练侧遗留);
- 合成夹具仅在 reviews/fixtures-eval-test/(标 synthetic,不混入正式数据);
- preflight --ready 在无 eval/test 冻结时必为 NOT READY(fail-closed),
  不生成可执行训练计划。
