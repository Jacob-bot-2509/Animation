# 预留题(holeout)题源清单

- 用途:未曝光辅助总体——校准/验证泄漏检测器,不进训练集、不开发、不审阅,仅当裁判。
- 原则:每条记录保留 来源/许可/年份/题号;纯本地,不对外传播。
- 状态:2026-10-06 已 clone 三个源(共约 1.4GB),提取管线待建。

## 1. 考研数学一真题(主力源)

- 仓库:https://github.com/TsekaLuk/Kaoyan-Math1-Papers (clone: kaoyan-math1/)
- 许可:CC BY-NC-SA 4.0;真题版权归出题单位(仅内部评测使用)
- 内容:papers/ 40 套(1987-2025,数学一;另含数学二 2024)+ solutions/ 逐题解析
- 格式:Markdown + LaTeX;解析为 (n)【答案】+【解】结构,与真题题号对应
- 质量:文字为主、少量图片题(如空间平面位置关系图)→ 图片题剔除出 holdout 池
- 注意:真题 md 有 OCR 噪声(空格/题号错位),解析质量较好;提取时需校验配对
- 预估题量:40 套 × 约 23 题 ≈ 900+

## 2. 北大课程考卷(libpku)—— 已验证,弃用

- 仓库:https://github.com/lib-pku/libpku (clone: libpku/,master,1.1GB)
- 许可:仓库无明确许可
- 验证结果(2026-10-06,工具 tools/holdout_verify_libpku_pdf.py):
  33 个 PDF 中 13 个文字版(线代 6/高数B 2/数分 5)、2 个 AES 加密、其余扫描版
- **弃用原因**:文字版全是"题面-only"考卷,无答案无解析;带答案的 PDF 是扫描版。
  按用户规则(完整三件套才入库)不可用,OCR 投入产出比低,不再投入。

## 3. Mufumoca 结构化题库(备用源)

- 仓库:https://github.com/Mufumoca/math (clone: math-bank/)
- 许可:仓库无明确许可;原始 HTML 压缩包未随库发布(版权原因)
- 内容:高数 4511/线代/概率/复变 共 8243 题,含题干/选项/答案解析
- 格式:**题目以 PNG 图片存储**(prompt/options/analysis 均为 img),文本源不在库中
  → 提取需 OCR,数学公式 OCR 误差风险高;**暂列为备用源,非主力**

## 提取管线计划(已完成 v1,2026-10-06)

1. ✅ 题面解析:papers md 按(大题节,局部题号)切题(填空题+选择题;解答题因节头被【解】污染暂不取)
2. ✅ 答案+解析:solutions md 按 (n)【答案】/【解】切
3. ✅ 配对校验:仅 (节,题号) 两侧对上且三成分齐全才出记录——缺题面/缺解析一律不要(用户指令)
4. ✅ 图片题剔除:题面含图片的题目未入池
5. ✅ 去重:与项目 297 对(现役+评测/测试)归一化比对,零精确重叠
6. ✅ 冻结:391 条 → kaoyan-pool-v1-manifest.json(记录级 SHA 绑定,FROZEN_UNEXPOSED)
   - 池本体 holdout-sources/extracted/kaoyan-triples.jsonl(gitignored,不入库)
   - 覆盖年份 1987-2021(2022-2025 因缺解析或格式变化,按"只有答案无题面的不要"排除)
   - 题量 391 ≥ 统计最小需求(299 负例 + 59 正例),有余量
7. 提取工具:tools/holdout_{scan,probe,extract,dedup,freeze}_*.py(已提交)

## 待办

- holdout v2 设计(Codex corrected-v2.md 口径):分层抽样、种子、盲标注角色、校准正例对构造
- libpku 33 个 PDF 的文本可提取性验证(次主力补充源)


## 与 holdout v2 设计的关系

- Codex corrected-v2.md 要求:未曝光总体、角色隔离、种子/分层、依赖处理、独立最终验证
- 本池解决"未曝光总体"的数据来源;其余要素(盲标注角色、抽样设计)待 Codex 口径后设计
- 校准正例对(同核心换数字题对)的构造方式待定(题源题配对/改造),不新写题
