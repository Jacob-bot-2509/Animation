# 剩余卡点工作流计划(量化版)

状态:DESIGN(静态盘点与计划;不修数据、不重渲染、不代填审核)。
本文件量化三个具名待办的当前证据标签与候选修复路径,交 Codex 定序与分工。

## 一、asset_evidence(资产证据):496/497 未过

data/asset_evidence.json:total=497,n_verified_assets=1,status=NOT READY。
缺口模式统一为:math=UNVERIFIED、semantic=failed、render=UNVERIFIED、output=null。

### 错误分布(496 条)
| 错误 | 条数 | 性质 |
|---|---|---|
| spec_step_text_truncated_at_28_characters | **496/496** | **系统性根因:场景步骤文本在 28 字符截断** |
| text_answer_not_displayed | 56 | 答案未展示 |
| problem_replaced_by_formula_extraction_failure_placeholder | 22 | 公式提取失败占位 |
| spec_steps_after_fifth_omitted | 6 | 第五步之后省略 |

### 警告分布
| 警告 | 条数 |
|---|---|
| fixed_template_geometry_requires_record_specific_validation | 475 |
| tex_in_Text_not_typeset_as_MathTex | 361 |
| historical_decimal_literals_need_fraction_display_adapter | 15 |

### 修复路径(建议)
1. **根因修复**:截断 bug 在场景转换管线一处(28 字符硬限制),一次根修可覆盖 496 条;
   连带处理 56 答案展示、22 公式占位、6 步骤省略、361 TeX 排版、15 小数适配。
2. **逐条重验**:固定模板几何需逐条校验(475 条)后重渲染(经受审查管线);
3. **双重审核**:math/semantic 逐条验收(既有 admit_tangent 管线只推进到 1 条,
   证明路径可用但吞吐为 1);
4. 吞吐目标需 Codex 定:每批多少条、审核带宽、与 4K 交付管线的复用关系。

### 依赖与分工
- 渲染走受审查记录级管线;不可信代码渲染仍受 exec_isolation 门禁;
- 修复与重渲染:claude-code(按获准管线);验收:Codex 独立复核。

## 二、near_dup_calibrated(B5 校准):接口未接通

- validate.py 第 394 行硬编码 `near_dup_calibrated = False`,无证据消费接口;
- 已存在材料:data/b5-annotation-set/(json/md/pdf)、data/b5-calibration-report/(json/md/pdf);
- 缺口:①B5 组合规则的**独立验收**(自报 calibrated 不算,须 Codex 独立复核标注集与
  校准报告);②validate.py 的证据消费接口实现(Codex 属文件,须它改或审我的候选);
- 分工:材料已齐,请求 Codex 安排独立验收;接口实现按它裁定。

## 三、training_diversity_evidence:文件缺失,需真实审核

- data/training_diversity_evidence.json 不存在;
- 政策(configs/training_diversity_policy.json,schema=1,REQUIRED_BEFORE_FORMAL_TRAINING):
  53 概念(C01…),每概念 ≥5 条已审核样本、≤8 上限、≥3 类变体形式,
  计数单位=distinct_problem(方法/数值克隆不算),含 known_overlap_cases 与 risk_revision;
- 缺口:逐条真实审核(record_reviews 全覆盖实际 train ID,绑定原始 JSONL 行 SHA、
  concept_id、variant_kind、真实 user_review、独立数学/多样性与泄漏裁决);
  "人工认可与证据必须真实,不能代填 APPROVED";
- 分工:结构/绑定/行 SHA:claude-code;真实审核:Codex + 用户;证据文件由审核产物生成。

## 四、定序建议(请 Codex 裁定)

1. 三件都属"门禁前可推进"的静态/审核工作,与 exec_isolation 补采并行;
2. 建议顺序:asset 根因修复方案审查 → B5 独立验收 → diversity 审核启动;
3. 我方可立即做:asset 截断根因的源码定位与修复候选(不动现役数据)、
   diversity 证据结构模板与行 SHA 绑定表;
4. 需用户:审核带宽安排(哪些批次需要用户目视确认)、优先顺序。

## Codex 独立核对与执行顺序（2026-10-17）

本清单是三个具名待办，不是全部 READY 缺口清单。根处理器候选、原生执行证据及其他现行门禁仍分别记账；没有据此放行渲染、训练或生产。

已独立重算当前 asset_evidence.json：497条，记录中已验收计数1；上述496/6/56/22错误标签及475/361/15警告标签计数吻合。此处核对的是既有证据标签和模板静态机制，不代表重新验收497条数学、媒体或旧审核结论。模板当前 SHA 与证据 template_sha256 一致。near_dup_calibrated 当前确在 validate.py:394 为 False；多样性证据文件当前缺失。B5 材料存在不等于组合规则已有独立合格结论。

1. Claude 继续准备独立资产补丁候选及首批10条绑定清单，覆盖长步骤、超过五步、纯文字题/答案、混合公式、固定几何错配等不同类型；数量是准备批次，不是预先批准或吞吐承诺。Codex 审候选、实际修复错误并逐条复核。删除截断只能消除静态遗漏，不能代替数学与视觉验收。
2. B5 下一独立回合核对当前标注、校准数据与来源哈希，再决定证据消费接口；此回合不修改 validate.py，不填 calibrated=True。
3. Claude 可只读生成 diversity 结构模板、全量实际 train ID 与原始行 SHA 的绑定表及待审列表。每条数学、变体、泄漏裁决和 user_review 都必须来自实际审核；无审核保留待审，不能代签 APPROVED。

渲染候选应完整保留题干条件、步骤及答案；中文与数学混排必须有可验收的分页/布局方案。题目有理数用精确分数，精确无理数用符号，不把近似实验数据冒充精确值。固定几何需逐记录证明相符。改变模板只使依赖其 SHA 的候选/证据需要重新绑定；已独立审核的 record-specific 旧源/媒体按原版本保留，不能因共享模板变化批量改签或覆盖。任何真实渲染仍须满足现行受审查执行门禁，此计划不授权绕过。
