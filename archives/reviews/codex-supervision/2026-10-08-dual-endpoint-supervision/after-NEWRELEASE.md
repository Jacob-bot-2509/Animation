# Animation Model Training v0.4.0

发布日期：2026-10-08
发布类型：验收材料封板版（Pre-release）

本版本同步数学动画训练项目 10-08 的进展：731 条数学复核收口、761 条语义签名与深层隔离裁决、原生真实公式渲染 165 条合格、真 4K 高清分页交付与全量逐页字形验收完成、训练超参数经实测语料重算并由用户确认落配置。生产门禁保持 CLOSED，训练未启动；沙箱双端实验现已开始采集，尚待双端原始材料对账；后续资格以各项独立验收结论为准。

## 本次交付

### 数据与语义

- 数学复核全部完成：731/731 条（22 批 v1/v2/v3 契约），Codex 独立复核通过。
- 语义签名 761 条 PASS：24 源、47 train / 264 selected_draft / 300 eval / 150 test，逐条绑定 record/math/source SHA。
- 深层隔离通道：1131 同族配对 → 12 候选逐对裁决（6 SAME_CORE 关闭、6 DIFFERENT_CORE）；Codex 结构性改写 4 条训练 ID（draft-c36-03、linalg-051、draft-c30-01、draft-c37-05，保留题数与编号），连同此前 c31-01/03、c18-02 修订，12 个具名配对局部关闭。全局语义隔离仍 NOT_ESTABLISHED（Codex 立场：零命中筛查不构成全局证书）。

### 原生真实渲染与高清分页（视觉验收线）

- 原生公式渲染：165 条合格（2711 条按题去重公式、5320 处原文出现，以当前交付索引汇总），本地 Manim 完整编译，逐条 record/math/source SHA 与视频 SHA 绑定。
- 高清修复历程：480p 单屏缩字（3 条过糊）→ 固定字号分页（626 页）→ **真 4K 分页最终交付：165 条 / 638 页（559 整页 + 79 分段）、3840×2160；本轮 19 条重渲染的 75 个页面起始帧与 PNG 逐像素一致，其余视频继承父交付验证并核对当前 SHA**。
- 全量字形逐页验收完成：638 页实际图像审阅 100% 覆盖、待审 0；期间修复 23 条记录（数学残留、表述歧义、LaTeX 截断、场景标签）与 3 条签名；98 题完整证明复审 + 96 项精确符号检查通过。资格 PASS_LOCAL_COMPLETE_CURRENT_FORMULA_PAGE_REVIEW。
- 定量记录：分辨率全 4K、165 条全覆盖，559 个完整页的每项占用包围盒高度代理最小为 92px。该代理不等同于最小字形高度，不能凭其大于 24px 宣称最小字形标准通过；逐页图像审阅资格另以 Codex 当前回执为准。
- 当前版本入口：reviews/codex-supervision/2026-10-08-complete-glyph-review/ 的 current-source-bindings.json、current-record-bindings.jsonl、current-complete-signatures.jsonl、CURRENT_DELIVERY_INDEX.jsonl（SHA b901df08…）。

### 训练准备

- 超参效率重算：实测训练侧语料 311 条 / 25.5 万字符 ≈ 0.3M tokens（哈希校验全过），推导并**经用户确认**：LoRA r16/α32、LR 1/5000 + cosine + 5% warmup、batch 2×4、seq 2048（构建期逐条校验拆分）、epochs 6 + 验收集早停、4bit NF4 双量化、paged_adamw_8bit；落配置 configs/hp_sweep.json（status=CONFIRMED、sha256 绑定、run=NOT_RUN_YET），首轮试训网格（1/4 数据 4 组）PLANNED。
- 训练流程约定（用户敲定）：小范围试训 → 生成动画渲染给用户看 → 用户自然语言提建议 → 数据/参数落地修改 → 迭代循环，用户点头才全量。
- 底座模型：Qwen3-4B（用户 2026-10-03 拍板，8G 显存 QLoRA 无溢出实测）。

### 协作自动化

- 双 AI 协作收件自动化：本侧每 10 分钟自动查信处理（含 Codex 修复交接规则），每 7 天自动续期；定义备份于 D:\code\.bridge-poll\cron-jobs-backup.md。

## 验证

- 数学/签名/渲染/分页/字形各线独立复验回执齐备，逐页 SHA 绑定；旧版目录全部保留作历史，不与当前入口混用。
- 本侧定量复测工具经历 Codex 三轮修正（标题污染、分段页口径、覆盖保护），当前权威量化口径以 Codex v3 为准（559 个完整页：最小值 92px / 第十分位最近秩 484/3 px / 中位数 658/3 px，均为每项占用包围盒高度代理）。

## 状态与边界

- production=CLOSED、PASS_CORE_SCOPE=false；全局语义隔离 NOT_ESTABLISHED；概念动画 NOT_EVALUATED（训练后评估）；原生沙箱 UNVERIFIED。
- 本版本不是训练完成或生产就绪版本。

## 下一步

1. 沙箱双端实验：当前 LAN 采集轮次 lan-2026-10-08-a，run remote-271e1c881c4f473fb027f5f28d4a3bd5，发送侧 complete=true、UNVERIFIED；收齐证人原始 JSONL、对应 summary 和真实退出码后对账。外部 IPv6 须另起唯一轮次并核实外部拓扑，不能沿用旧日期轮次。操作单 reviews/2026-10-07-witness-runbook.md。
2. 实验对账与 Codex 独立验收。
3. 训练数据集构建（含 seq 2048 逐条校验）→ 首轮试训网格 → 动画样本交用户目视。
