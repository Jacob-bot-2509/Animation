# 资产证据 496 条根因报告(只读定位,未改任何文件)

状态:ROOT_CAUSE_LOCATED_NOT_FIXED。结论:496/497 资产未过的根因全部集中在
tools/render_templates.py 的 `_steps_block`/`_answer_block`/`_title_block`。

## 逐条对应(证据→代码)

| 证据错误/警告 | 代码位置 | 机制 |
|---|---|---|
| spec_step_text_truncated_at_28_characters(496/496) | `_steps_block` 第 61 行 `Text({step[:28]!r}, …)` | **硬截断 28 字符**,连 LaTeX 都切半(实测:'第二步…$(2,'、'$S = \\fr') |
| spec_steps_after_fifth_omitted(6) | 第 59 行 `enumerate(steps[:5])` | 只渲染前五步 |
| tex_in_Text_not_typeset_as_MathTex(361) | 第 61 行整段塞 `Text()` | 步骤里的 $...$ 以原文形式显示,不用 MathTex(与模块 docstring"公式用 MathTex"相悖) |
| text_answer_not_displayed(56) | `_answer_block` 第 70-72 行 | answer 无 $...$ 段时 `_math_segments` 返回 None → 直接 wait 不显示答案 |
| problem_replaced_by_formula_extraction_failure_placeholder(22) | `_title_block` 第 49-52 行 | problem 无公式段时标题变成"(公式段提取失败)"占位 |
| fixed_template_geometry_requires_record_specific_validation(475) | 模板整体 | 固定几何模板需逐条校验(已知设计限制) |
| historical_decimal_literals_need_fraction_display_adapter(15) | 数据侧 | 小数→分数显示适配 |

## 修复候选(未实施;实施须先审,因 template_sha256 是资产证据绑定)

`_steps_block` 三处:
1. 删除 `[:28]` 截断,完整步骤文本;
2. 删除 `steps[:5]` 限制,渲染全部步骤(或按 max_steps 显式参数,不静默省略);
3. 混排渲染:把步骤按 `$...$` 切段,中文段 `Text`、公式段 `MathTex`,
   用 VGroup 排列——同时消掉 tex_in_Text 警告;

`_answer_block`:answer 无公式段时用 `Text(answer)` 兜底显示(消 text_answer_not_displayed);
`_title_block`:提取失败时用 problem 原文作标题兜底(消占位警告),仍如实记录提取失败。

## 影响与前置

- render_templates.py 的 SHA 是 asset_evidence.json 的 template_sha256 绑定;改模板
  → 全部资产证据须按新 template_sha256 重生成/重渲染/重审核(496 条)——正是
  blockers-workstream-plan.md 的 asset 工作流,吞吐与批次待 Codex 定。
- 场景源目录 assets-current-v3/sources/ 属旧 three-gates 根,修复后新产物必须落
  新 cohort 根(根处理器方案已交),不能在旧根上覆盖。
- 修复候选与审查顺序:Codex 审模板补丁 → 我按获准补丁改 → 重生成+重渲染 →
  Codex 逐批验收。
