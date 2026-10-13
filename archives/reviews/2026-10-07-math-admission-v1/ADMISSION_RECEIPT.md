# 30 题数学修订接入层(独立新版本 + 场景/来源绑定)

对 Codex 严格修复交付(reviews/codex-supervision/2026-10-07-core-submission-supervision)
的接入。不覆盖原包、旧回执、现役数据、选择器、冻结 54 项。

## 1. 独立重推导(全部通过)

- 30 条 = train 9 / eval 9 / test 12,分布在 5 个现役源文件
- 5 个现役源文件 raw SHA 与修订包 before 绑定全匹配
- 逐条:现役记录 dense SHA == before_record_dense_sha256;仅替换 changed_fields 后
  dense SHA == after_record_dense_sha256 == corrected_record
- corrected-sources 候选版逐行核对:变更行精确对应修订后记录,未变更行逐字节保留
- 工具:tools/verify_math_corrections_30.py

## 2. 场景字段版本绑定(本轮新增)

Codex 指出"沿用的场景字段可能仍对应旧题文"。对 30 条场景字段做令牌比对:

| 结论 | 条数 | 明细 |
|---|---:|---|
| 场景需更新 | 7 | prob-038(0.6/0.4/0.2→3/5/2/5/1/5)、prob-042(p=0.5→一般p+公平附加条件)、eval-calc-027-s3(删除0.85914数值校验主线→交换次序+代换)、eval-prob-007-s2(k=23临界点/小数→精确递推乘积)、eval-prob-007-s3(期望≈1.19推理→二阶矩+柯西下界435/799)、eval-prob-008-s3(0.0569→精确q与差值式)、test-prob-008(3.5/0.1→7/2与1/10) |
| 场景一致(含说明) | 23 | prob-046 为形式化改写,场景分割故事仍数学一致;linalg-050 数字差异为平凡假阳性 |

- 更新层:scene-updates-candidate.jsonl,每条含新旧场景 SHA、理由、数学字段绑定
- 接入版源文件 admission-sources/:以 corrected-sources 为底,仅替换上述 7 条记录的
  scene_spec(及 2 条的 visual_style);dataset_calc/dataset_linalg 两文件与
  corrected-sources 字节等同;7 条更新行经 dense 复核,23 条未改记录核对一致
- 自检工具:tools/build_math_admission_v1.py、tools/verify_math_admission_v1.py

## 3. 旧渲染回执不得作为新版本证明(如实列明)

以下渲染/场景产物均基于修订前数学字段,修订版渲染须另行生成:

- dataset_audit_2026-10-05-render-check(/render-check-r2) 全部 HTML 渲染包
- reviews/2026-10-06-scene-standard-sweep batch1-10 场景草稿
- reviews/codex-supervision/2026-10-06-scene-repair-takeover 场景修复候选 v2/v4/v5
- reviews/codex-supervision/2026-10-04-metadata-pdf-fix 渲染证据(test-calc-027)

详见 scene-binding-audit.json。

## 4. 仍未建立(不伪装通过)

- 30 条数学修订的最终准入尚待 Codex 独立复验本接入层
- 剩余当前题目实际数学复核、核心范围同核心隔离判定仍待执行
- 本接入层不含任何渲染结果;场景更新后的渲染需在新版本上重做

## 5. 请求

请 Codex 独立复验本接入层(30 条数学修订 + 7 条场景版本绑定),裁定是否与
CORE_SCOPE_ONLY 一致。当前状态:PENDING,production CLOSED,qualification UNKNOWN。
