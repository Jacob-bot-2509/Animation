# 候选数据集入场契约(DATASET_SCHEMA)

> 2026-10-02,msg_152。配套实现:src/animtrain/dataset_intake.py +
> tools/dataset_intake.py(convert/check/report)。
> 本契约管"候选数据 → 正式样本入口"这一段;数据验收仍需走
> make_manifest → data_check → split → freeze → preflight 全链路。

## 1. 样本入口:只接受 JSONL

- **正式样本入口只有 JSONL**:一行一个 JSON 对象(train/eval/test 的样本
  语义按行定位)。当前正式输入为 `data/v1/raw/*.jsonl`(63 条)。
- `dataset_*.json`(项目根目录)仅为**原始数组容器/待转换**,不得作为
  train/eval/test 入口;入场检查对 JSON 数组直接拒绝(硬伤)。
- **JSON 数组整文件是"待转换"格式**,不得被误当正式样本通过。
- 转换路径:`tools/dataset_intake.py convert <数组.json> <输出.jsonl>`
  —— 内容零清洗、原文件只读、默认拒绝覆盖已有输出(显式 --force 才覆盖)。

## 2. 正式字段(其余键一律 quarantine 提示)

| 字段 | 语义 | 缺失处理 |
|---|---|---|
| id | 全局唯一样本 ID(str/int) | 硬伤 |
| category / sub_category | 模块分类(如 数学分析/极限) | 硬伤 |
| problem / solution | 题干与解答(可含 $...$ LaTeX) | 硬伤 |
| answer | 可判分终答(缺失 → quarantine 候选) | quarantine |
| scene_spec | objects/steps 动画规格 | 硬伤 |
| source | 来源(当前全部 self-authored) | 硬伤 |
| license | 许可证,白名单见 §4 | 硬伤 |
| function_family / visual_style / efficiency_tags | 可选元数据(缺失/空 → quarantine,候选语义) | quarantine |

## 3. ID 唯一性

- 同 ID 同内容 = **整条重复**(硬伤);同 ID 不同内容 = **ID 冲突**(硬伤)。
- 工具只报告"文件:行号"可定位清单,**绝不静默改名/去重**——真实数据的修改
  由用户确认后执行。

## 4. license 语义(白名单 + 内部研究使用)

- 白名单:apache-2.0 / mit / internal-generated / cc-by-sa-4.0。
- `Internal-Research-Use-Only`(当前 63 条全部如此):**仅限内部研究使用,
  不公开分发,后续转正**。用户已于 2026-10-02 确认该语义,故列入白名单;
  它不代表满足 Apache/MIT/CC,数据公开前必须先转正为真实许可证。
- 白名单外的其他值 → 硬伤(未声明语义)。

## 5. LaTeX 规则(只报告,不改写数学语义)

- `$...$` 公式内出现中文 → **硬伤**(TeX 无 CJK,渲染必失败);中文一律放
  Text()/公式外。
- 疑似漏反斜杠(`+infty`、裸 `arctan`/`lim`/`sin` 等)→ **quarantine
  (render_risk)**,报告区分"语法/渲染风险"与实际渲染失败;
  工具绝不自动改写公式内容。

## 6. 同题多解设计(P1#6,预留契约)

- 预留字段:**problem_id**(定位题目)、**solution_id**(定位一种解法)、
  **method**(解法命名,如 squeeze_theorem / polar)。
- 同一 problem_id 多条记录 = 同题多解;动画与 solution_id 一一对应。
- 当前不要求自动制造多解;schema 预留只为后续同题多解数据可直接入场,
  不破坏现有 id 唯一性契约。

## 7. scene_spec 契约与动画验证状态(P1#7)

- scene_spec 必须含 **objects / steps** 两列表(当前 63 条均齐备),
  但它只是**设计稿**,不是已验证动画。
- `code` / `render_status` / `code_sha256` 缺失 = **动画未验证**;
  状态如实标 **candidate/UNVERIFIED(候选)**,不得宣称动画已验证、不得假绿。
- 验证后状态才可升级:code 过 render_gate、render_status=verified、
  code_sha256 登记。

## 8. 状态语义

- 入场检查状态:clean(无问题)/ candidate(有 quarantine)/ rejected(有硬伤)。
- **candidate ≠ 已验收训练集**:入场检查 clean 只说明数据契约通过,
  manifest 生成只登记事实,均不代表数据已验收。
- 当前审查结果见 DATASET_REVIEW.md(63 条:数学分析 19、概率论 9、
  解析几何 12、高等代数 23;入场检查 clean)。
- 等待 Harness 对修正后 63 条跑出新结果后,再决定 split / freeze /
  preflight READY;在此之前保持 candidate/UNVERIFIED 语义。
