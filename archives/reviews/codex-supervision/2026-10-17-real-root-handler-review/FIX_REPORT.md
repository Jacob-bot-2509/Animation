# 根处理器与新增工作流邮件复核

本轮结论：根处理器已由 Codex 修复，39 项独立 unittest 方法通过，资格仅限“完整注册表的供给事实策略检查 + 本机受控元数据处理”。不接入现役执行器，不创建实际 ROOTS，不作原生沙箱验收。

活动运行：start-03653094452c414fa4835fd37cb0c7c7。
邮箱运行：run-dc16b5a77ed048bc8538fbe3b3d89d9a。
邮件：876、878、880、881。邮件是待审材料，不扩权。近期只读观察器心跳与 HEAD 见 observer-status.json；4 项历史 core_drift 不能冒充本轮新缺陷。进程存在本身不证明任务进展。

## 876：修复与独立验证

改前源码、作者50项回执、测试完整保存在 before/；原作者回执没有覆盖。old-defect-reproduction.json 实际复现8项旧错误：空 cohort 可写、目录本身可写、未传实际回执仍通过、COM1.txt 被接受、混合反斜杠被接受、SHA尾换行被接受、已存在目标被接受、新根未经 REGISTERED 可直接 ACTIVE。

Codex 修改 exec_native_roots.py、test_exec_native_roots.py，新增 README.md 和 exec-native-roots-receipt.v2.json。具体绑定见 source-bindings.json，完整修后版本见 after/。

- 完整 v2 schema、严格类型与规范 Windows 相对路径；拒 ADS、点段、设备名扩展、反斜杠别名及大小写绑定冲突。
- 独立当前工具哈希、完整 bound map、独立保管的上一快照原字节与 SHA；校验单步历史删除/改写/跳转，新根必须 REGISTERED。冻结历史保留原 cohort。
- 写入要求整个 cohort 的规范 SHA、ACTIVE 根和闭合子路径；child 不能写父端 raw。实际回执须与可信预期 root/run/cohort 完全一致，不把旧冻结回执当当前新作业。
- 元数据预留以 (cohort SHA, job UUID) 为身份；项目内既存未冻结 base，检查重解析点/冻结祖先；mkdir 原子占位，独占意图文件、fsync 和原子替换。不同 cohort 的同名 job 不冲突；同一对身份重复拒绝。
- 损坏文件、崩溃占位、残留锁与临时文件保留 UNCERTAIN，不自动擦除/重试。FINALIZED 只说明本地元数据状态转换，不证明执行成功。

测试真实输出见 test-run-2.stdout.txt / test-run-2.stderr.txt：39 个方法全部通过；含 6 进程同键竞争仅1成功、16线程竞争、完成状态竞争、损坏/缺失意图、替换失败、冻结祖先及重解析事实拒绝。测试只运行已审查的固定处理器/固定测试代码，项目内临时目录清理前校验边界。test-run-1 的1项失败来自测试预期仍要求损坏意图产生锁；实现已在写锁前保守拒绝。测试修正为核对文件未改变及状态仍 UNCERTAIN，未放宽策略。

接口有意破坏旧弱调用：不再接受裸 entries 代替完整注册表；写入/回执必须提供独立上下文；finalize 必须同时提供 cohort 与 job。尚无现役调用接线，README 说明新接口。

仍未实现：恶意同权进程下句柄约束/ACL/TOCTOU 安全边界、目录级断电持久性、可信历史 tip 的长期保管/防多步回滚、真实原生根注册/创建/执行器接线与原生验收。lstat 和本机并发通过不能代替这些证明。

## 878 / 880 / 881：统计核对与文书修复

已直接检查现行模板、validate.py、资产证据与多样性政策，并将原字节保存在 inputs/，哈希见 input-bindings.json。independent-blocker-census.json 从当前资产记录重算：

| 标签 | 条数 |
|---|---:|
| 总记录 / 证据自报已验收 | 497 / 1 |
| 28字符截断 | 496 |
| 第五步之后遗漏 | 6 |
| 文字答案未展示 | 56 |
| 题干被公式提取失败占位替代 | 22 |
| 固定模板几何待逐题核验 | 475 |
| TeX 放在 Text | 361 |
| 小数字面量待核对 | 15 |

标签计数与邮件吻合，模板当前 SHA 与证据记录一致。以上不是重新验收全部497条数学/媒体或复签那1条旧验收。near_dup_calibrated 确为 validate.py:394 的 False；training_diversity_evidence.json 当前不存在。

Codex 已修改 blockers-workstream-plan.md 与 asset-evidence/root-cause-report.md，纠正“全部根因仅在三处”和“这是全部 READY 缺口”的过度结论，并补齐完整题干/步骤/答案混排、分页、字体/定界符、固定几何逐题对应与精确分数显示的候选验收要求。不能只删除截断然后默认完整画面合格；模板变化按实际依赖重新绑定，保留独立 record-specific 的既有源/媒体和审核原件。

已与 Claude 确定准备顺序：资产共同根因候选与首批10条多故障覆盖绑定 → B5独立验收及消费接口 → diversity绑定表/待审材料。Claude 可做只读准备及独立候选，不覆盖现役模板/数据，不代填 APPROVED。首批10条是候选准备规模，不是审核吞吐保证或渲染执行许可。

878/881 当前裁定为修正文书后的静态发现与计划合格；880 的执行与实际审核仍 NEEDS_EVIDENCE。B5标注/校准的当前逐项合格结论、消费接口、多样性实际数学/变体/泄漏和用户审核均未在本轮完成，不填 calibrated=True，不代签任何人。

## 归档与边界

本报告、前后快照、真实失败/通过输出、原始输入、邮件快照及真实回信记录由 delivery-manifest.json 冻结绑定；兼容目录保存相同字节，供既有邮箱 ACK 使用。完成交接后要求 Claude 按修复版本继续后续候选准备，不重复改已完成部分。

前一 IPv6 runbook 审查已单独冻结于 archives/reviews/codex-supervision/2026-10-17-ipv6-runbook-review/，回信 msg_1792231327973_877；本轮新增根处理器不覆盖该归档。

没有修改现役模板、validate.py、资产证据、原生收发/采集工具、模型配置、调度器或冻结历史；没有探针、实际原生根接入、渲染、训练、Git提交或上传。D2/D8 继续 deferred GAP，不阻塞训练准备；production=CLOSED，全局隔离 NOT_ESTABLISHED。后续新邮件/活动信号保留给下一次监管。
