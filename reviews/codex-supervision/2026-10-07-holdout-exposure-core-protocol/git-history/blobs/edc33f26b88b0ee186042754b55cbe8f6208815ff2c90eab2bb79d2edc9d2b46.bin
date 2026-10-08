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

## 2. 北大课程考卷(libpku)

- 仓库:https://github.com/lib-pku/libpku (clone: libpku/,master 分支,进行中)
- 许可:仓库无明确许可,来源为各课程资料;内部评测使用
- 内容:高数 B 99 张考卷、线性代数 30+ 卷、数学分析考卷+答案(另有 130+ 非数学课程忽略)
- 格式:PDF 为主 → 需 pdftotext 提取后评估文本质量(扫描版则弃用)
- 预估题量:约 1000+(待提取确认)

## 3. Mufumoca 结构化题库(备用源)

- 仓库:https://github.com/Mufumoca/math (clone: math-bank/)
- 许可:仓库无明确许可;原始 HTML 压缩包未随库发布(版权原因)
- 内容:高数 4511/线代/概率/复变 共 8243 题,含题干/选项/答案解析
- 格式:**题目以 PNG 图片存储**(prompt/options/analysis 均为 img),文本源不在库中
  → 提取需 OCR,数学公式 OCR 误差风险高;**暂列为备用源,非主力**

## 提取管线计划(kaoyan 优先)

1. 解析 papers/*.md → 逐题拆分(选择题/填空题/解答题,选项 A-D)
2. 解析 solutions/*解析/*.md → (n)【答案】+【解】逐题拆分
3. 题号配对校验(每套题数一致、无缺号)→ 生成记录:
   {id: holdout-src-kaoyan-<year>-<n>, problem, options, answer, solution,
    source_repo, source_path, year, question_no, license, subject}
4. 剔除图片题(题面含 ![]() 且图片承载信息者)
5. 与项目 264+47+497 全部记录做哈希/内容去重
6. 输出未曝光辅助总体池(JSONL),加锁冻结

## 与 holdout v2 设计的关系

- Codex corrected-v2.md 要求:未曝光总体、角色隔离、种子/分层、依赖处理、独立最终验证
- 本池解决"未曝光总体"的数据来源;其余要素(盲标注角色、抽样设计)待 Codex 口径后设计
- 校准正例对(同核心换数字题对)的构造方式待定(题源题配对/改造),不新写题
