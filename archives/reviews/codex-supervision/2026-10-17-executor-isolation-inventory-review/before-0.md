# 真实执行器与判定器合同(设计稿 v1)

状态:DESIGN(未接线、未实现、不运行)。依据 docs/READINESS-EVIDENCE-PROTOCOL.md §6.1。
本文件只定合同,不把 v2 固定夹具 scope 改成 production 使用。

## 1. 组件与调用边界(§6.1)

| 组件 | 职责 | 边界 |
|---|---|---|
| converter(受审查转换器) | scene_spec → scene.py | 白名单模板渲染,生成物是数据不是工具指令;禁任意代码拼接/字符串 eval;输出 scene.py 与转换日志,各自独立 SHA |
| renderer(白名单渲染器) | 执行 scene.py 产出真实媒体 | 父进程启动;AppContainer + JobObject 实际证据;超时/内存/输出根约束;仅白名单编译器/渲染器 |
| judge_math(受限数学判定) | 逐断言 verdict + 完整理由 | 受限 DSL + 精确分数字符串;禁 eval/exec/任意 SymPy 求值入口;未定 = UNVERIFIED |
| judge_fidelity(画面忠实判定) | 逐项按锁定清单核对真实画面 | 每项时间/帧定位 + 判定理由;AI/API 仅在获准调用范围,不出网不读密钥 |

**生效前提**:exec_isolation(§2)验收合格前,不可信生成代码一律不真实运行;本合同在
该前提满足后才可执行真实渲染/判定。

## 2. 接口合同(扩展 v2 response-index)

- CLI:`executor --request <request.json> --work <work_root>`;真实 rc、原始 stdout/stderr、超时。
- request.json:沿用 eval-evidence-v1 键;evaluator_sources 扩展 converter/renderer/
  judge_math/judge_fidelity 四组件绑定(path + sha256 + protocol_role);limits 增加
  max_memory_mb、max_output_bytes、per_question_timeout_seconds。
- response-index.jsonl 逐样本(identity 含 split/problem_id/sample_id/row_index):
  - input_bindings:{input_record_sha256, generated_spec_sha256, scene_py_sha256,
    conversion_log_sha256}——转换前后都绑定
  - render/executable/math/fidelity 四 stage:decision(PASS|FAIL|UNVERIFIED)+reason_code
  - artifacts:[{path, sha256, size, media_type(png/mp4)}]
  - rc、timeout、parent_evidence:{job_object_record, token_evidence, profile_cleanup,
    acl_restore}——各为证据文件路径(父进程核验存在+ SHA,不信自报)
  - math.assertions:[{id, statement, verdict(bool|null), reason}]
  - fidelity.items:[{item, frame, verdict, reason}]
- 父进程核验:v2 全部拒绝清单(身份/rc 真实性/spec 漂移/产物根内/SHA/非空/解码/
  rc0 无产物/断言覆盖/重复/额外/缺失/超时/路径逃逸/陈旧回执)之外,新增:
  scene_py 与 conversion_log 的 SHA 与回执一致、parent_evidence 文件真实存在且 SHA
  一致、E 的 PASS 集 ⊆ R 的 PASS 集。

## 3. 数学断言受限 DSL

- 断言 statement 仅允许:白名单运算符(+ - * / ^)、精确分数字符串、有理数比较、
  集合/区间成员、真值表项;禁任意 sympify/eval。
- 判定结果三分:PASS(断言成立且理由完整)/FAIL(假命题或条件缺失)/UNVERIFIED
  (无法判定,如 CAS 未定)。UNVERIFIED 不转 PASS 不转 FAIL。
- 题目答案字符串不直接当动画数学正确(§6.3 M 定义)。

## 4. 画面忠实清单(F)

- 每固定题锁定 checklist:[{item, frame, assertion}];判定逐项给 verdict + 理由 +
  实际帧定位。
- 清单缺失或无法核对 → 该题 F=UNVERIFIED;抽帧/公式编译成功不宣称全动画忠实。

## 5. 接线验收序列(§6.4 后半)

1. 本合同经 Codex 独立审查并定稿;
2. exec_isolation(§2)验收完成后,实现 converter + renderer(白名单)与 judge_math;
3. 最小集成复验:真实媒体 + token/job 回执,固定题单可复算 R/E 逐题合同;
4. 只有该版本通过,才把 eval_step 从恒返 2 改为"正式评测完成且绑定有效时返 0";
5. hp_sweep 与 harness 消费同一核验报告;M/F 接口先留 UNVERIFIED,独立审查机制
   落实后再扩。

## 6. 未决与如实局限

- 渲染器与既有 4K 交付渲染管线(资产验收已完成)的复用关系待定;复用须 Codex 复验。
- MP4 解码校验当前协议未定义(现有实现仅 PNG);定义后另行接入。
- judge_fidelity 的 AI/API 调用范围未获批,当前设计只允许人工判定器或获批范围。
- 本设计不改变 v2 夹具的 fixture-only 边界;正式四指标仍全部 UNVERIFIED。

generated_by: claude-code
generated_at: 2026-10-17T12:04:25+08:00
