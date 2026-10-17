本目录当前提交：generation-4dd25e9e717e4cd0b18f2e679841b401/。旧顶层 math-correspondence.jsonl 保留原字节，不能把它当当前版本。

build_math_correspondence.py 是审查定位工具，不作数学判定，不执行场景。它复用已审 content-geometry-mapping 的严格源绑定，扫描题干、解答、答案以及全部 scene_spec.objects/steps；输出带完整源文本、位置、公式和保留全部字符的语句片段。数字字面量转为 Fraction 只表示该字面量的精确有理值，不表示原量就是精确值，也不把有限小数猜为某个简单分数。符号分数必须另核分母和定义域；未支持语法显式待审。所有抽取 verdict=PENDING_REVIEW。

使用项目 venv 的 Python -X utf8 -B 执行构建器，输出到全新 generation-UUID 目录，最后由 COMPLETE.json 绑定文件哈希；拒绝源失配、输入漂移、项目外路径和冻结输出。完成标记不是断电持久性或恶意并发写者隔离保证。21项独立回归通过。

特别区分两个版本：
1. 本目录的新抽取代仍绑定当前原题库，保留其原始小数/旧措辞，供审查对账，不宣称原题已修复。
2. Codex已完成十题数学修订候选，位于 archives/reviews/codex-supervision/2026-10-17-first-batch-exact-math-review/candidate/records.jsonl。题号及数量不变，题干/过程/答案/场景文字按精确数学修订，逐题源/原始行/数学内容/候选哈希在同目录 record-reviews.json。35项手写表达式精确计算核验通过。实际渲染、字体/公式编译、原生布局、全动画几何对应和用户目视仍待验。

后续按修订候选准备逐题实现和真实审阅材料；不能把原抽取代的源哈希或旧媒体套在新候选上，也不能直接把候选放行到训练。候选若进入新的数据版本，须重新绑定所有受影响的源、清单、锁、媒体与审查证据。现役题库、模板和旧冻结材料本轮不覆盖。

完整报告：archives/reviews/codex-supervision/2026-10-17-first-batch-exact-math-review/FIX_REPORT.md
