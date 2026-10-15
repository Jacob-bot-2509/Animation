# 当前公式交付与审阅进度（2026-10-08，本轮两处修复）

当前索引覆盖 **165条记录、633页，3840×2160**：[CURRENT_DELIVERY_INDEX.jsonl](../codex-supervision/2026-10-08-determinant-glyph-followup/CURRENT_DELIVERY_INDEX.jsonl)。SHA256：667278f661c3a0ca3f72b415a914d2cfc73845dad8f3987d31a38e82b32af715。

Codex已修复 eval-linalg-004-s3 的拆列行列式记号和 eval-linalg-002-s3 的三阶余子式展开方向标签。题目和正确答案保持不变。完整300条eval候选位于 [dataset_eval-final-candidate.jsonl](../codex-supervision/2026-10-08-determinant-glyph-followup/dataset_eval-final-candidate.jsonl)，保留上批3题修复，本轮仅再修2题。

当前记录版本由 [current-record-bindings.jsonl](../codex-supervision/2026-10-08-determinant-glyph-followup/current-record-bindings.jsonl) 唯一选择；761条记录、24个物理来源。先前候选与原始数据文件作为历史，不能越过当前绑定选择旧版本。完整复验与资格见 [FIX_REPORT.md](../codex-supervision/2026-10-08-determinant-glyph-followup/FIX_REPORT.md) 和 [final-independent-verification.json](../codex-supervision/2026-10-08-determinant-glyph-followup/final-independent-verification.json)。

- 本批核对8题的完整证明、实际查看32张原PNG及5张重渲PNG。当前32页合格。
- 累计实际逐页审阅 **296/633页**，尚余 **337页待审**：[current-unreviewed-pages.json](../codex-supervision/2026-10-08-determinant-glyph-followup/current-unreviewed-pages.json)。本批逐页结论与精确公式、PNG及记录摘要绑定。
- 当前633页尺寸、SHA、几何和源码公式绑定均验证；新5页独立解码核对视频像素，其他628页按相同公式、几何、PNG继承原像素证据。
- 当前完整公式页552张重新计算占用高度代理：最小92，第10百分位最近秩484/3，中位数219；1080高最小代理46。81张分片排除。这些值不能证明最小字形高度。
- **全部字形验收NOT_ESTABLISHED，最小字形高度NOT_CERTIFIED，概念动画NOT_EVALUATED，全局语义隔离NOT_ESTABLISHED，原生沙箱UNVERIFIED，生产CLOSED。**
- 本轮活动中文说明的编码已恢复。以下历史说明保留原字节，其旧数量和路径不得覆盖上面的当前交付。

---

# 视觉验收证据包(作者侧·结构验收;人工目视复核待完成)

范围:TRUSTED_LOCAL_MATHTEX_ONLY 的 165 条合格渲染记录
(权威清单 = reviews/codex-supervision/2026-10-08-real-formula-followup/qualified-records.jsonl,冻结目录未做任何改动)。

## 本包内容

| 文件 | 说明 |
|---|---|
| frames-manifest.jsonl | 165 帧抽帧清单:mp4 SHA 逐条复核通过 + 帧 SHA + 亮度自检 |
| frames/、frames-jpg/ | 每条记录的视频首帧(场景 t=0 起静态,首帧即最终画面) |
| frame-metrics.jsonl | 每条:墨点量、内容包围盒、24px 行带数、裁边检查、质心 |
| frame-summary.json | 异常汇总(裁边/偏移/低行带/疑点明细) |
| visual-acceptance-report.json | 逐条结构结论 + 方法 + 局限声明 |
| contact-sheets/sheet-01..14.png | 每页 4×3=12 格、带 id 标注的接触片,供人工目视 |
| suspect/(空,疑点帧逐帧剖析仅在需要时生成) | — |

## 自动结构验收结论(作者侧)

- **165/165 PASS**:每条视频首帧有实际墨迹(≥200 像素@亮度>32)、内容居中、无边缘裁切。
- 首轮亮度阈值 128 曾报 3 条"近黑"(draft-c01-03、draft-c18-02、prob-040):
  诊断后确认**非空帧**——这 3 条公式组含超宽长式,整组等比缩小,细笔画抗锯齿后亮度低
  (包围盒宽仅约 140px)。内容完整在框内,但 480p 下**字号很小**,人工目视须放大看。

## 人工目视复核指南(未完成,待你或 Codex)

1. 打开 contact-sheets/sheet-01..14.png 过一遍 165 格:公式可见、无乱码方框(tofu)、无截断。
2. 重点放大看 3 张:draft-c01-03(38 式)、draft-c18-02(49 式)、prob-040(40 式)
   —— 对应 frames-jpg/ 下同名 jpg。
3. 结论写回本目录(新文件,勿覆盖),逐条标注 VISUAL_PASS / VISUAL_FLAG。

## 诚实声明

本包只证明**结构层面**:真实公式视频确有内容、布局正常、未裁切。
**字形级目视核验(符号正确性、字体回退、渲染瑕疵)本环境无法执行,故 human_visual_review=PENDING。**
receipt 中的 visual_acceptance 不得因此包从 NOT_REVIEWED 改为通过——除非有人实际看过了。
