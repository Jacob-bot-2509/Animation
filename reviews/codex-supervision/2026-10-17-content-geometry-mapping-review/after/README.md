本目录是首批 10 题的静态内容映射候选，不能批准数学、几何、动画或训练。

当前有效输出：generation-738cbabf9d634db386237a246c3ab940/。
该目录的 COMPLETE.json 绑定 mapping.json、逐题 JSONL 以及输入版本。旧顶层 content-geometry-mapping.jsonl 保留原字节，仅作历史材料；generation-1112a2c2a96b4937b6e7ed63d94f2cfa 是本轮中间版，不作当前交付。

用项目 venv 的 Python -X utf8 -B 执行 build_content_mapping.py 即可生成新的 generation-UUID 目录。输出仅新建，不覆盖旧目录；失败留下的无 COMPLETE 目录不作为完成交付。输出标记不承诺断电持久性或恶意并发写者隔离。

构建时验证当前首批清单、证据文件、旧模板、已加载候选模板、选择器及源文件 SHA；逐条验证源行、原始行 SHA、记录 SHA 和题号。空批、非 10 条、重复题号、失配、未知模板、构建期间可见的输入变化均拒收。旧几何清单只对应 REVIEWED_LEGACY_SHA256 指定的模板版本；模板更新后需要重新审查清单。

每题同时保存完整步骤计划及题干→所有步骤→答案计划。片段起止位置可还原源字符串；coverage 仅说明文本片段完整，原生字号、公式编译、实际分页仍待独立验收。词语命中只记录原文位置，不证明数学对象或几何正确。旧模板的固定图形逐项列为 PENDING_REVIEW；文本候选没有修好旧几何。

数学与几何结论保留 PENDING_REVIEW，user_review 保留 null。不能代签用户目视结论。历史源记录可能含小数，映射保留原字节，不通过显示替换冒充数学修订；新编写的几何参数使用精确分数或数学表达式。

独立回归：test_content_mapping.py，23 项通过。完整归档及具名限制：
archives/reviews/codex-supervision/2026-10-17-content-geometry-mapping-review/FIX_REPORT.md
