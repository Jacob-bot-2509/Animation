# Claude Code后续交付约定

本轮接手的错误已由Codex修复并归档。请使用effective-core-v2/source-bindings.json中的24源和record-bindings.jsonl中的761个真实版本；配套签名为revised-complete-signatures-v2.jsonl。仅c18-02数学版本变化，不能混用它的旧签名或旧渲染验收。66条签名文字补正也应整体接入，保留提交原件。

签名打包示例（从项目根执行，选择未存在的新输出目录）：

    .\.venv\Scripts\python.exe -X utf8 -B tools/core_signatures.py bundle --group current-761-v2 --input reviews/codex-supervision/2026-10-07-semantic-signature-supervision/revised-complete-signatures-v2.jsonl --out reviews/2026-10-07-semantic-core-lists/current-761-v2-new

完整候选筛查也使用同一输入及新--out。rc0表示绑定/候选生成完成；rc3为显式部分覆盖，rc2为输入/绑定错误。任何退出码、零候选均不是全局隔离许可。

下一批只需补当前761记录的结构候选和逐对理由：按数学目标、对象/定义域、关键假设、核心变换及证明结构审查同义和数值变式；不以标题或步骤字符串不相等排除泄漏。无需全历史语料、旧36条链或全盘扫描。发现问题由Codex复核并另版修订；不要删除题、只改数字掩盖同核心或擅自合并进入现役。

新c18题的浏览器排版/视觉证据需引用新record_sha256/math_sha256。760条原记录可通过真实哈希继承旧数学材料，但不能把旧761条整体渲染回执当作新题渲染通过。

用户最新安排：Codex不负责双端实验；实验及操作单由Claude Code处理。本轮后续只交付数学、签名、局部配对和版本归档。双端材料不作为本轮新增交付要求，也不由本轮审查标绿。

数学及签名修订范围已合格；全局semantic_isolation=NOT_ESTABLISHED、native=UNVERIFIED、production=CLOSED、PASS_CORE_SCOPE_issued=false。下一批材料按此范围继续提交，Codex给出绑定版本资格并归档。
