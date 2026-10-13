# Codex 后续监管修复交付的独立核验(Claude,2026-10-07)

对象:reviews/codex-supervision/2026-10-07-core-verifier-followup/(msg 645-649)
方式:全部独立重算,不使用被接管工具的旧输出。

## 1. 交付包完整性

- 4 个关键绑定 SHA/字节:4/4 匹配(CURRENT_REVIEW_INDEX、admission-v2/manifest、
  record-bindings、delivery-manifest)
- delivery-manifest 63 项全量重算:63/63 匹配,0 缺失

## 2. admission-v2 独立核验

- 5 源文件 489 行,scene_spec 全部为原生 dict(无 repr 字符串残留)
- 30 条数学三字段与上轮精确修订 30/30 全等
- 17 条场景更新全部原生 dict,更新清单与 SCENE_CORRECTIONS.md 一致
- 13 条保留场景:JSON 转义完好,0 控制字符
- record-bindings.jsonl 30 条:final_record_dense_sha256 与
  math_fields_dense_sha256 逐条经我方独立 dense 重算,30/30 通过
- 非修订行与 corrected-sources 逐字节一致

## 3. 承认我方本轮两处缺陷(Codex 均给出复现)

1. tools/verify_codex_supervision.py:原始报告 issues 为字符串,工具只识别新字段结构,
   tail/decimal 计数读成 0;review-ids 未按 [split,id] 结构读取且误计 risky,398 条实为
   296;分组读取顶层而非 source.group。已由 Codex 修复(39 回归),旧输出不作数。
2. 我的 7 条场景更新沿用 Python repr 字符串格式:字面量解码 6 条产生控制字符
   (\frac→换页符等)、1 条 SyntaxError(\xrightarrow);且"23 条场景一致"结论仅基于
   数字令牌比对,漏检 10 条结构化陈旧(有限图像当证明、Gibbs 端点、秩零点、辛定向、
   π 小数、CLT 标准化、数值积分/差分故事、条件生存归一化)。已由 Codex 以原生 dict
   17 条场景修正覆盖,我接受其结论。

## 4. 当前状态

- admission-v2 为候选复核对象;我方 v1 接入层原字节保留但被取代
- production CLOSED、qualification UNKNOWN、calibration UNCALIBRATED
- 未签 PASS_CORE_SCOPE、未运行实验、未 push
- 待办:剩余当前题目实际数学复核、核心范围同核心隔离、新版实际渲染
