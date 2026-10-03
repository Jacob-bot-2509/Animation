# eval/test 准备接口(EVAL_TEST_PREP)

> 2026-10-03,msg_197。**只准备 schema/目录/验收脚本接口**;
> eval/test 尚未生成、尚未冻结——本文档不把未生成的内容写成已冻结。

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
  eval/      README 占位——未生成任何 eval 样本
  test/      README 占位——未生成任何 test 样本
```

- eval/test 样本生成时必须写**新文件**,绝不覆盖 raw 或原始 JSON;
- 生成后走:make_manifest → data_check → freeze(锁绑定 manifest)→
  preflight --ready。

## 3. 验收脚本接口(tools/eval_test_prep.py,已实现只读部分)

- `status` — 报告 eval/test 是否已生成/已冻结(当前恒为"未生成/未冻结");
- `check <dir> [--train-dir]` — 已生成样本时:入场检查 + 与 train 的
  精确重叠(核心正文哈希)与近重复(5-gram Jaccard,阈值 0.7 UNCALIBRATED)隔离检查;
  未生成时如实报"未生成"(exit 0,不视为检查通过);
- `freeze <dir>` — **未授权:一律拒绝(exit 2)**;正式 freeze 在用户批准后
  经 freeze_data 执行。
- 报告契约:0 = 未生成(如实)或检查通过;1 = 硬伤(泄漏/坏样本);2 = 未授权。

## 3.5 JSONL schema(eval/test 样本契约)

eval(同题多解)单行:

```json
{"problem_id": "eval-p001", "solution_id": "eval-p001-s1", "method": "方法名",
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

- eval:未生成、未冻结;
- test:未生成、未冻结;
- 合成夹具仅在 reviews/fixtures-eval-test/(标 synthetic,不混入正式数据);
- preflight --ready 在无 eval/test 冻结时必为 NOT READY(fail-closed),
  不生成可执行训练计划。
