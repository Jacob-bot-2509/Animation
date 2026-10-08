# Claude Code 当前数学交接

使用 effective-core-v3/source-bindings.json 全部 24 源、record-bindings.jsonl 的 761 个实际版本及 revised-complete-signatures-v3.jsonl。四个改写 ID：linalg-051、draft-c36-03、draft-c30-01、draft-c37-05；身份与题数保留，757 完整记录不变。冻结父版和现役不覆盖，不回退已修工具或混用旧签名。

数学与场景文字、签名对应合格；61 项具名工具回归、46 项新符号检查、6 项一般性证明通过。12 个修订具名方法记录配对局部合格，另 6 个未改候选为局部不同核心；全局 semantic_isolation=NOT_ESTABLISHED。

原 162 回执为常量空 MathTex，撤销公式通过结论。已修 tools/native_render_pilot.py；完整公式、实际变量、真实绑定、不可覆写、完整日志与视频 SHA、失败非零退出码具备。Codex 7 条实际样例／180 公式条目通过。需你重交的当前 156 个 ID 和版本在 native-resubmission-requirements.json。

从项目根调用，选尚不存在的新输出目录：

    .\.venv\Scripts\python.exe -X utf8 -B tools/native_render_pilot.py --ids <本批ID...> --out reviews/2026-10-07-native-render-pilot/<新批名>

每批交 run-inputs.json、receipt.json、完整公式清单、实际 scene.py、stdout/stderr 和实际视频。失败退出码 3，输入／绑定错 2。不能删掉错误项后声称原范围全过，不能复用旧空模板视频。无需重交历史语料。

深层通道只找同族候选，不排除未命中／跨族；逐对工具要求候选 SHA、完整实际重算及版本化理由。新的跨族／同义／嵌入子任务候选继续交 Codex 独立裁决，不能只改数值或步骤名称。SAME_CORE／NEEDS_REVIEW 返回 3。

双端实验按用户安排由你负责，不在 Codex 本轮执行或验收范围。视觉、概念动画、原生隔离／生产证据不据此标绿；production=CLOSED，PASS_CORE_SCOPE_issued=false。
