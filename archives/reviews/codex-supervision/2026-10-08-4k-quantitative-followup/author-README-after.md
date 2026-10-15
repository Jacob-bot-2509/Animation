# 当前视觉复核入口（2026-10-08）

当前交付为 **165条记录、633页、3840×2160**。权威索引是 [DELIVERY_INDEX.jsonl](../codex-supervision/2026-10-08-glyph-review-followup/DELIVERY_INDEX.jsonl)，SHA256为 `07b4543d38599e1c30d2b515e0c2a8761e5611f771c46c75ee23b357c58b6331`。上轮已修复9条记录的22处分数数组公式，实际逐页复验其45页，该目录保持冻结。

本轮新证据见 [FIX_REPORT.md](../codex-supervision/2026-10-08-4k-quantitative-followup/FIX_REPORT.md)、[current-quantitative-corrected.json](../codex-supervision/2026-10-08-4k-quantitative-followup/current-quantitative-corrected.json) 和 [page-glyph-verdicts.jsonl](../codex-supervision/2026-10-08-4k-quantitative-followup/page-glyph-verdicts.jsonl)。

- 当前633页均绑定实际PNG路径和SHA。公式区域占用包围盒高度除以该页显示项数，最小值为92像素，第十分位数（最近秩定义）为160像素，中位数为677/3像素；折算到1080行画面，最小槽位代理值为46像素。
- **槽位代理值不等于最小字形高度**。上标、下标、分数和矩阵内部必须依据实际图像核验，不能用槽位超过24像素推导字形全部合格。
- 当前同版本实际逐页证据覆盖144/633页，其中120页继承具名冻结证据，本轮新增24页。剩余489页见 [unreviewed-pages.json](../codex-supervision/2026-10-08-4k-quantitative-followup/unreviewed-pages.json)。本轮实际查看预览为2048×1152，原PNG为3840×2160，不据此签发原生最小字形尺寸证书。
- `readable-pages-verification-4k.json` 是此前626页版本的作者原始量化材料，保留作溯源。它未提交槽位算法及逐页SHA字段，其槽位数值与本轮具名公式区域算法不一致；不同指标不能直接互换，不能用于关闭当前633页的全量字形验收。
- 当前本地高清布局与页面绑定通过；**全量字形验收仍为NOT_ESTABLISHED**。概念动画NOT_EVALUATED、全局隔离NOT_ESTABLISHED、原生沙箱UNVERIFIED，production=CLOSED。单项通过不能扩展为整个项目合格。

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
