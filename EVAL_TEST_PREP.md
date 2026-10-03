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

## 3. 验收脚本接口(占位,未生成样本前不可执行)

- `tools/eval_test_prep.py`(接口预留):
  - `check` — 对 eval/test JSONL 跑入场检查 + 与 train 的精确重叠/近重复隔离检查;
  - `freeze` — 生成 *.lock.json 并绑定当前 manifest(冻结后哈希变化大声失败);
  - `status` — 报告 eval/test 是否已生成/已冻结(现在应恒为"未生成/未冻结")。

## 4. 当前状态(如实)

- eval:未生成、未冻结;
- test:未生成、未冻结;
- preflight --ready 在无 eval/test 冻结时必为 NOT READY(fail-closed),
  不生成可执行训练计划。
