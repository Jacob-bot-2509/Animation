# 评测接线候选实现 v1(无模型固定夹具)

对应 docs/READINESS-EVIDENCE-PROTOCOL.md §6。独立候选目录,不改 eval_step.py、
不改真实模型/超参、不训练、不接真实渲染/判定器。

## 文件与 SHA

| 文件 | SHA256 |
|---|---|
| eval_protocol.py | (见 evidence-index.json) |
| fixture_executor.py | (见 evidence-index.json) |
| run_fixtures.py | (见 evidence-index.json) |
| fixture-receipt.json | 20 场景 × 期望/结果矩阵 |

## 实现范围(§6.1/6.2)

- `build_request`:request.json 合同键(protocol_version/run_id/round_id/candidate_id/
  scope/SHA 双向绑定/evaluator_sources/limits/fixed_questions)
- `verify_bindings`:启动前 executor 源 SHA 与 generated-specs SHA 绑定校验,漂移即 REFUSED
- `run_executor`:白名单绑定后真实子进程启动(非 shell=True、非任意命令串),
  采集真实 rc/stdout/stderr,超时即停
- `verify_response`:逐样本核对——身份(缺失/重复/额外)、rc 真实性(自报与真实
  returncode 比对,拒绝 bool 冒充整数)、spec 漂移、产物(根内路径/SHA/非空/真实解码)、
  rc0 无产物强制 FAIL、数学断言逐条覆盖(必需断言 id+布尔 verdict+理由,假命题 FAIL、
  未定 UNVERIFIED)。父进程重算,不信任回执自报 VERIFIED
- `aggregate`(§6.3):Q_s 按 split+problem_id 计题,S_q=题内全部必需样本;任一必需
  样本失败→该题失败;缺证据→该题 UNVERIFIED 且整指标 UNVERIFIED、rate=null;
  精确分数(Fraction);E 的 PASS 集 ⊆ R 的 PASS 集校验;by_split 双列

## 夹具矩阵(§6.4 最小清单,20 场景)

fixture-runs/<scenario>/ 每场景独立 work 目录,含 request.json/response-index.jsonl/
artifacts/executor.stdout/stderr/eval-report.json。场景与结果见 fixture-receipt.json:
01 全绿基线;02 真实 FAIL 分母(5/6);03 缺 ID;04 重复 ID(首行一并作废);
05 额外 ID 拒绝;06 executor 源 SHA 漂移 REFUSED;07 spec 漂移;08 损坏媒体;
09 空媒体(强制 render FAIL);10 rc0 无产物(强制 FAIL);11 超时;12 路径逃逸
(完整性拒绝);13 数学假命题(M=5/6);14 数学未定(M 整指标 UNVERIFIED);
15 F 清单缺失(F UNVERIFIED);16 同题多场景其一失败(题 FAIL);
17 rc=bool 冒充整数(全拒);18 rc 伪造(自报 0 实退 3,全拒);
19 坏 schema(E 该题 FAIL);20 executable 失败(E=5/6)。全部 E⊆R 成立。

## 如实局限(接线前须解决)

1. **默认拒绝为真**:任何未绑定进 request 的 executor/judge 一律拒绝启动;当前只有
   fixture_executor 一个绑定对象,不是真实渲染/判定器。
2. **重解析点检测**:仅 resolve+前缀判定;完整 reparse-point 逃逸检测须按
   witness_transfer_common.checked 既有实现接入(§6.2 父进程拒绝清单的完整版)。
3. **M/F 判定器未实现**:数学断言只做"覆盖+布尔裁决+理由"的结构校验,不证明数学
   为真;F 只校验清单存在与裁决字段,不核对真实画面。真实 judge 接线另行立项。
4. **媒体解码仅 PNG**(PIL);MP4/其他如实 UNVERIFIED。
5. **AppContainer/JobObject 父进程证据**不在夹具内(真实执行隔离属 §2 exec_isolation,
   未验收前不可信生成代码不得真实渲染)。
6. **generated-specs 的 row_index 字段**:eval_step.py 现有导出不含 row_index,
   正式接线时须补齐并重新绑定(§6.2),不在本候选改动。

## 验收口径

本候选只证明"协议骨架 + 父进程拒绝清单 + 分母/未知/精确分数语义"在固定夹具下
行为正确。接线验收(把 eval_step 恒返 2 改为绑定有效时返 0)须 Codex 对本版本独立
复验后另行执行;真实 executor/judge 接线、真实媒体与 token/job 回执按 §6.4 后续
最小集成复验另做。
