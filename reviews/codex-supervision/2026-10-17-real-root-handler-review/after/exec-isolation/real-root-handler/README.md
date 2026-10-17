# 根处理器候选 v2 的资格与接口

状态：LOCAL_METADATA_AND_SUPPLIED_POLICY_FACTS_ONLY；不接入现役执行器，不创建实际 ROOTS，不授权采集或运行生成代码。

Codex 修复了旧 v1 的空 cohort 绕过、只核对 verifier 的伪 cohort、无实际回执仍通过、设备名/反斜杠/换行路径别名、existing_paths 空操作、新根直接 ACTIVE、畸形对象崩溃及任务路径与身份问题。原作者回执 exec-native-roots-receipt.json 保留不变，只描述原版本；新版本使用 exec-native-roots-receipt.v2.json。

- check_registry_entries 的第一个参数现在是完整 v2 注册表，不能继续传裸 entries。必须另传 current_tool_hashes 和 previous_snapshot_bytes；后者是调用方独立保管的上一份原始字节。
- check_write(reg, root_id, write_rel, cohort_digest, *, current_bound_map, current_tool_hashes, history, existing_paths, reparse_paths, writer="parent") 返回 (ok, reason)。cohort_digest 是整个 cohort 的规范 JSON SHA256，不是 verifier SHA。history 为原始字节。仅 ACTIVE 可写；child 不能写 raw。
- check_receipt_root 同样要求完整上下文，另传 receipt={root_id,root_path,run_id,cohort_sha256}。run_id 必须等于独立预期的32位小写十六进制 ID。当前资格只接受 ACTIVE 的新作业，不把冻结旧回执升格为当前回执。
- HistoryChain 检查完整 schema、重复 JSON 键、精确原字节 SHA、不可改历史字段和单步状态。调用方仍须保管可信最新 tip；本模块不能证明该 tip 未回滚。
- JobReservation(base) 的 base 必须由可信父进程选择，是项目内已经存在、未冻结的元数据目录，不从待执行内容采纳。reserve(cohort_sha256, job_uuid32)、finalize(cohort_sha256, job_uuid32)、inspect(...) 均绑定同一对身份。唯一原子 mkdir 保留占位；不能用不同 cohort 的意图完成另一个任务。
- 损坏意图、缺失意图、中断锁和临时文件均保留 UNCERTAIN，不自动清理、重试或回收。FINALIZED 仅表示本地元数据转换完成，不证明子任务成功、证据合格或生产可用。
- 已做 lstat 检查重解析点、硬链接文件、冻结祖先，并以独占文件写意图、文件 fsync、原子替换和跨进程争用测试验证本机正常环境行为。但未实现句柄约束的 TOCTOU 防护、恶意同权进程隔离、ACL 证明、目录断电持久性或持久可信 tip，因此不能作为原生安全边界或接入凭证。

独立验证：39 个 unittest 方法通过，含旧缺陷反例、6进程同键争用（仅1成功）、16线程争用、文件中断/损坏注入。临时目录只在项目内，经边界检查后清理。实际原生根、探针和现役工具没有运行或修改。production=CLOSED。
