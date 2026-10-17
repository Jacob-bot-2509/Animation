# 资产证据 496 条根因报告(只读定位,未改任何文件)

状态:ROOT_CAUSE_LOCATED_NOT_FIXED。结论:已识别的共同文字遗漏与格式缺陷可定位到
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
  → 依赖该模板的候选需重新绑定与验收(当前496条待审标签)——正是
  blockers-workstream-plan.md 的 asset 工作流,吞吐与批次待 Codex 定。
- 场景源目录 assets-current-v3/sources/ 属旧 three-gates 根,修复后新产物必须落
  新 cohort 根(根处理器方案已交),不能在旧根上覆盖。
- 修复候选与审查顺序:Codex 审模板补丁 → 我按获准补丁改 → 重生成+重渲染 →
  Codex 逐批验收。

## Codex 修订：静态根因成立，完整资产结论尚未成立

已直接检查当前 tools/render_templates.py，确认 _steps_block 的 [:28]、[:5]、全段 Text，_answer_block 无公式时只 wait，以及 _title_block 无公式时使用占位。已独立核对当前证据标签数量与本表相同。不能从标签数量推导“全部根因只在这三处”：数学正确性、固定几何对应、文本布局、公式字体及实际媒体仍需独立验证。

候选修复验收必须补全以下条件：

- 仅删除 [:28]/[:5] 会使长段或更多步骤超出画面。需要完整内容的分页/逐屏布局，逐页内容映射和所有步骤覆盖证明，不能改为更小字号后默认可读。
- 标题即使能提取数学段，当前实现仍丢弃非公式题干条件。标题和答案都应保留完整文字及公式、混合片段顺序；纯文字兜底只是其中一种情况。不能以公式段替代完整原题。
- 混排需处理转义美元符、数学定界符、换行、中文字体与 LaTeX 构建时序；简单正则切分或 VGroup 排列本身不是验收。异常须明确失败，不能悄悄删段。
- 15条小数字面量警告需回到题文/证明核实哪些是精确有理数，再以分数显示；原始日志、帧时序和测量值保留原样，不盲目转换或估算。
- 475条固定几何警告需逐记录验证或改为与记录绑定的实现；解决文字缺失不证明动画概念正确。

模板变更后的重生成/重验范围按实际 source/template SHA 依赖确定。1条已有 record-specific 审核不应被自动重签或覆盖；旧源、媒体、审核原件保留。候选进入首批10条静态复核；未经后续执行门禁与具体授权，不重渲染、不使用旧冻结根。本次只修正候选文书及独立元数据处理器，没有修改现役模板或资产证据。
