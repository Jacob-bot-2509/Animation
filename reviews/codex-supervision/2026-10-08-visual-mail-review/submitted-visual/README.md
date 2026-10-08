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
