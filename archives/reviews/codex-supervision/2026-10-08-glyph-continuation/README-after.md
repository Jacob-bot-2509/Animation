# 当前视觉复核入口（2026-10-08，v3工具修复后）

当前交付为 **165条记录、633页、3840×2160**。权威索引是 [DELIVERY_INDEX.jsonl](../codex-supervision/2026-10-08-glyph-review-followup/DELIVERY_INDEX.jsonl)，SHA256为 `07b4543d38599e1c30d2b515e0c2a8761e5611f771c46c75ee23b357c58b6331`。9条记录的分数数组行距修复沿用该冻结交付，本轮题号、数学正文和视频未改动。

本轮修复及独立证据见 [FIX_REPORT.md](../codex-supervision/2026-10-08-quantitative-v2-review/FIX_REPORT.md)、[verification-v3.json](../codex-supervision/2026-10-08-quantitative-v2-review/verification-v3.json) 和 [independent-v2-review.json](../codex-supervision/2026-10-08-quantitative-v2-review/independent-v2-review.json)。

- `tools/visual_acceptance_verify_pages.py` 已改为原生RGB公式区域度量，不缩半、不把标题当公式、不四舍五入。像素区域、阈值、含端点包围盒及精确统计定义完整写入候选JSON；异常返回非零，要求指定新的输出路径，拒绝覆盖原件或写入冻结归档。
- 633页的真实PNG/几何SHA、4K尺寸及顺序绑定通过；完整公式页552页、分片81页。仅552完整页计槽位代理：最小92像素，第十分位数484/3像素（最近秩），中位数219像素；最小代理折算到1080行画面为46像素。分片标NOT_APPLICABLE，不混入统计。
- 原v2 JSON增加了真实路径/SHA和顺序配对，633页绑定经独立核对通过。但其旧源码按缩半整帧计算，包含页标题；报告还将偶数样本上中位数2897/10冒作中位数，按原已舍入值计算的正确算术中位数应为579/2。原JSON、源码与前后补丁均保留，新候选不会覆盖原件。
- **槽位代理不等于最小字形高度，也不是符号或分片完整性认证。** 原生画布边缘墨迹检查只判结构，不能据此推导全量视觉通过。
- 同版本实际逐页证据当前覆盖209/633页：170页从具名同版本证据继承，本次实际新增39页（29页完整公式、10页分片；分片仅判可见部分且全部核对伴随页）。其余424页见 [unreviewed-pages.json](../codex-supervision/2026-10-08-glyph-continuation/unreviewed-pages.json)。本次逐页理由与SHA见 [page-glyph-verdicts.jsonl](../codex-supervision/2026-10-08-glyph-continuation/page-glyph-verdicts.jsonl)，续审报告见 [REVIEW_REPORT.md](../codex-supervision/2026-10-08-glyph-continuation/REVIEW_REPORT.md)。预览为2048×1152，原PNG为3840×2160，不据此签发原生最小字形尺寸证书。
- **当前仅本地版本绑定、结构和量化工具修复合格，全量字形仍NOT_ESTABLISHED**；概念动画NOT_EVALUATED、全局隔离NOT_ESTABLISHED、原生沙箱UNVERIFIED，production=CLOSED。

`readable-pages-verification-4k.json` 属于修复前626页，`readable-pages-verification-4k-v2.json` 属于633页旧量化工具；二者为历史原始材料。当前完整算法和精确候选以本轮v3证据为准，不能混用各版统计或把结构PASS当全量字形PASS。

以下为早期165视频首帧包的历史说明，其首帧和接触片入口不替代当前633页索引与逐页审查。

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
