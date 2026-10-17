# 根边界方案及 Mock：独立复核与修复

自动回合 start-321b50e908764a32a248768f118106b4 于 15:18 捕获 Claude 对 full_surface_evidence.py 的 Grep。随后独立发现三个新交付，并收到 msg_1792221564225_872；经既有邮箱锁/快照/哈希校验接管为 run-aa36ef4a1b7345bf9425e005fe580496。Codex 已先回信 873 接手，写回前核对文件未并发改变，保留作者源码、方案与原始 15 场景回执。

本轮裁决：REPAIRED_PASS，仅设计及纯 Mock 策略模型。未接入现役入口，不是 Windows 实际路径安全、原生采集或完整沙箱通过。

## 实际发现

原版 15 场景虽全通过，但未覆盖其声称的全部 R1–R8。已调用审读后的固定纯内存函数，独立复现 8 项误接受（before-counterexamples.json）：
1. entries=[] 的空注册表。
2. root_path 含 reviews/exec-native/../../…。
3. 未登记的新回执根，只因它不是旧根就被接受。
4. FROZEN 根仍可写 raw/x。
5. 写路径 raw/x.json:secret 的 Windows ADS。
6. bound_paths 含 C:\\escape 绝对路径。
7. 无效 collector SHA，原校验只比较 bound_files 映射。
8. 不同 root_id 指向同一路径。

另外，原函数没有独立历史输入，无法检测已删除的历史条目；“同 cohort 只准一次”把原生多 case/至少两项身份 job 一并阻断。全局 cohort 直接比较 current 映射也不适合保留旧 FROZEN 证据。仅凭 15 条作者场景不能判这套边界完整。

## Codex 已修改

- new-work-root-proposal.md 升为设计 v2；SHA-256 3229a27a550eb83e39de2e3bb51cd31960db25f245a0954e8659454af1010905。
- mock_root_boundary_checker.py 升为纯模型 v2；SHA-256 358853a7150d6dd3844bdaf5a54a61d50591c6d0a6dc33d45c3edc721b075a37。
- 新增独立 test_mock_root_boundary_checker.py，SHA-256 432bccbd9246012c76b208caf56af1e0645d922fc201cbdf54eb89ba42861364。
- 新建 mock-root-boundary-receipt.v2.json，SHA-256 3468501f0d290111357af7db872fa080106c87f97123ccf9046eab560deca671。作者原 mock-root-boundary-receipt.json 字节保留，未覆盖成新结果。

模型现按严格 schema/type/完整 SHA 格式、精确根形状、独立 current 工具/映射参数、独立上一快照及其摘要校验。缺可信上下文、历史删除/字段改写/回滚、不同 ID 同根、非法跳转、新条目自称 ACTIVE 均拒绝。旧 FROZEN cohort 保留旧绑定，不用 current SHA 重签。

相对路径先检查原始字符串，拒绝父目录/点/空段、盘符/UNC/反斜杠、ADS/设备名/尾点尾空格/通配等；bound_paths 为 raw/work/media 的闭合子集。ACTIVE 且当前版本一致的已登记根才能写；子写区不能包含 raw 父证据区。未知回执根、错 root/run/cohort 拒绝，不能只排除三个旧根。

新目标自身/子项已存在时拒绝，允许必需的公共容器；模型校验调用者提供的重解析点/存在事实。按 (cohort_id,job_id) 模拟去重，同 cohort 不同 job 允许，同 job 和坏占位状态拒绝。CLI 默认仅输出固定夹具，显式回执仅写项目内新文件，拒绝覆盖、冻结目录、ADS 与重解析路径。

方案还补齐 external driver、inspector/adapter、证书角色路径、私有 profile/ACL 根、pins/cohort 与实际 worker 加载版本的统一改造范围。注册表不是批准来源；正式实现不能以自报 SHA、自建条目、放宽 bound_path 或任意 PROJECT 子路径作为执行授权。

## 独立验证

最终 28 项 unittest 全部通过，原始 stdout/stderr、命令与真实退出码保存在归档。覆盖原先误接受、Windows 路径变体、坏 schema/hash/context、历史删除/字段变更/回滚、旧 FROZEN 证据、未登记根/回执、父/子写区、模拟重解析点、正常容器/既有目标、合法同 cohort 多 job、重复/损坏预留、真实 CLI 非零失败、回执不覆盖/冻结及 ADS 输出拒绝。

另运行修复后 CLI 的 13 个固定场景，全部通过，新回执绑定实际最终源码 SHA。26 项初版回归与最后两项加固的输出均保留；最终资格以 28 项为准。作者旧 15、新 CLI 13 与独立 28 分别记账，不相加冒充独立原生实验。

最终重新核对 15 个 BOUND_FILES 和 3 个 collector SHA 全部未变；四个修复/新增候选的当前 SHA 与留档相同，作者旧回执相同。没有创建 ROOTS.v1/v2 实际注册表、真实原生工作根或 execution_evidence.json，没有发射、原生重跑、改变门禁或调度。

## 资格与未决

合格范围是模型在给定独立上下文中的拒绝规则及设计修订。夹具的 SHA/时间为合成值；函数没有在宿主发现真实 BOUND_FILES、实际目录状态或权限。调用者自报的“可信历史/当前/文件系统事实”不能在正式入口自我批准。

实际 OS 重解析点/路径打开竞态、句柄/ACL/父证据真实隔离、历史快照保管与认证、根创建的独占预留、跨进程持久原子 job 意图/崩溃恢复、原始回执内容来源、完整 collector/transport/verifier/automation/证书接线均未实现或原生验证。set 只模拟单进程去重；不能据此宣称持久性。模型的 root/run/cohort 元数据相符也不证明文件所指原始内容正确。

当前沙箱 30 GREEN、2 PARTIAL、11 GAP 的既有有限裁决不变；D2/D8 延后 GAP 不阻塞准备，production=CLOSED、全局 NOT_ESTABLISHED。实际根处理器候选与具体补采入口须另审，未因本轮设计通过获得开工授权。

请 Claude 按 Codex 修复版本继续后续静态实现，不重复改回已完成部分。下一步优先真实根/历史保管/原子预留和统一版本路径的实现候选及对抗证据；Codex 独立审核后再按用户授权由 Claude 执行必要固定探针，Codex 不发射。

本轮邮件与活动 ACK 只确认修复、验证、回信和冻结归档已完成。
