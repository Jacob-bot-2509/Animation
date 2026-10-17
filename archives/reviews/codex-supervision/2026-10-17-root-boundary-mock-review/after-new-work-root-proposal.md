# 新工作根与统一边界方案（设计稿 v2，Codex 修订）

状态：DESIGN_REVIEWED_WITH_MOCK_ONLY。只修订方案与纯内存校验候选；没有创建真实 ROOTS 注册表、新原生工作根、运行探针或证书，也未改 BOUND_FILES、现役 collector/transport/verifier。

原版“15 场景通过”未覆盖 R1 空登记、路径规范化、冻结写入、真实历史删除等缺口。Codex 已保存原版并复现 8 个误接受，修复模型后增加独立对抗回归。旧 mock-root-boundary-receipt.json 作为历史原件保留，新回执另名，不覆盖。

## 1. 现状和适用范围

现役 sandbox_execution 与 full_surface_evidence 的 WORK_ROOT 固定 three-gates；后者 REVIEW_ROOT 与 sandbox_surface_acceptance.HERE 固定 all43，production_isolation_acceptance.OUT 固定 three-gates。sandbox_external_test_driver.REGISTERED_ROOT 与 inspect/adapter 的范围、证书 raw/surface 路径、私有 profile/临时 ACL 的真实授权根，也必须纳入统一设计，不能仅改其中几个常量。

现有 registered adapter 的实例内读集合收窄与 job 输出仅用于受限对账，不是采集或通用路径旁路。当前证书不存在，既有 30 GREEN、2 PARTIAL、11 GAP 的范围不因本方案改变；旧 named-window 资格只按其实际绑定继承。

## 2. 注册快照、可信上下文和状态

未来可提独立 reviews/exec-native/ROOTS.v2.json，但本轮不创建。注册表结构与 Mock schema 对齐：
- schema=exec-native-roots-v2，entries，previous_registry_sha256；
- 每 entry 严格包含 root_id、root_path、purpose、cohort、bound_paths、status、created_at；
- root_id 为最多 64 个小写 ASCII 字母/数字/下划线/连字符，首位字母或数字；root_path 精确为 reviews/exec-native/run-<root_id>；
- purpose 是 transport/surface/joint/external 之一，不填竖线拼接字符串；
- cohort 为 collector_sha256、verifier_sha256、bound_files_sha256_map；所有 SHA 为完整 64 位小写十六进制，实际映射必须由可信父进程从受审查完整 BOUND_FILES 独立取得；
- bound_paths 是 raw/work/media 的非空无重复子集，不能是任意目录或通配；
- created_at 为带时区的实际登记时间；夹具中的合成时间只用于模型测试，不是实际登记；
- 新 entry 只能 REGISTERED；只许 REGISTERED→ACTIVE→FROZEN 或同状态保持，FROZEN 不可回滚。

注册表不是执行批准来源。独立受审查配置/具体授权限定 collector、verifier、用途、实际操作与可选 root_id；请求自报路径、当前 SHA 或自建注册条目都不批准执行。正式实现必须绑定操作所需的根角色、完整源码集合和批准来源，不能让模型自行选根。

注册快照保存前版本 SHA；可信父进程提供独立固定的上一完整快照，检测历史删除、复用 ID/路径、字段改写和状态回滚。只在请求里附一份“历史”并与自己计算的 SHA 对上不是可信历史。真实版本链需由受审查保管入口、访问控制及原字节固定，不能把可改 latest 指针当权威。

旧 entry 的 root/path/purpose/cohort/bound_paths/created_at 均不可改。已 FROZEN 的旧 cohort 保留原 SHA，不拿新 current 映射回填；FROZEN 仅表示记录封存，不等于验收合格。活动 cohort 与实际代码漂移必须拒绝继续使用。

## 3. 路径、写权限与并发

项目相对路径先验证原始字面量，再使用路径 API：拒绝 ..、.、空段、绝对/盘符/UNC、反斜杠别名、ADS、设备名、尾点/尾空格和通配。不能先用 Path 折叠掉证据后只做 startswith。根必须精确匹配登记，未知新路径不因“不是旧根”而通过。

新根与旧工作根、其他登记根及其祖先/子树不得重叠；新目标已存在或含既有子项应拒绝。但 reviews/exec-native 这个正常公共容器本身必然已存在，不能把它当所有新根都冲突。已登记根的生命周期不因其创建后“已存在”而自我失效。

实际 OS 重解析点、祖先、权限和路径打开时竞态须在正式实现中于真实使用时验证。Mock 仅检查调用者独立提供的 existing_paths/reparse_paths 事实，不访问目标目录，不证明实盘无 junction/symlink 或 TOCTOU 已解决。未经证明的事实不能按空集合假设为真。

只有 ACTIVE 且当前 cohort 一致的已选根可写。模型规定父进程可写登记的 raw/work/media，子进程不能写 raw 父证据区；正式实现仍须真实 ACL/句柄/令牌隔离、源文件与产物清单前后绑定、进程树停止后固化证据。单纯“目录名字不同”不提供权限隔离。REGISTERED 预留不是任意写入许可，FROZEN 不可写。

cohort 是同版本的一批验收/补采上下文，不等于一个原生 job。两项身份对照及多 case 都需要同 cohort 的不同 job；因此按 (cohort_id,job_id) 防止同一 job 重复，而不禁止整个 cohort 再有别的合法 job。Mock 的 set 只模拟单进程占位，不具备跨进程原子性、持久化或崩溃恢复。正式启动前需独占锁和持久意图/唯一 job 预留，结果不确定时保留占位，不盲目重跑。

## 4. 回执与旧证据兼容

当前轮根/回执检查须绑定精确 root_id/root_path、可信预期 run_id 和 cohort 摘要；未知根、旧路径、错 run 或错 cohort 均拒绝。当前 Mock 只检查这些身份元数据，不能证明回执实际文件的来源、内容、父证据或数学/媒体正确；正式验收还须验证完整原始载荷及逐文件 SHA、受信任来源和用途/角色。

旧冻结原件按 (path,sha256,原 schema,原实现绑定,具名窗口/协议) 只读解释；新活动根拒绝把旧原件冒充本轮新实测。旧有限 LAN D9 可以按既定适用性审查作为组件候选，不强制无依据全量重跑，也不自动升级到新轮/新实现。

证书的 transport_root_id 与 surface_root_id 等实际角色需显式对应受审查快照，raw_path/surface_raw_path 逐一在各自精确允许集合中；不能以任意 PROJECT 子路径为兜底。新增合同须版本化保留旧读取器/原件语义，不给旧原件重签当前 SHA，不修改已冻结目录。

## 5. 拒绝矩阵与已经实现的模型范围

| 规则 | 当前模型与独立回归覆盖 |
|---|---|
| R1 未登记 | 空/错 entries、缺可信上下文、未知 root_id、未知回执根拒绝 |
| R2 路径冲突 | 根精确形状、旧根/登记根重叠、不同 ID 同路径、既有目标/子项、正常容器区别 |
| R3 版本绑定 | collector/verifier/完整映射格式与独立当前参数匹配，不信 entry 自报当前版本 |
| R4 写越界 | Windows 规范相对路径、ACTIVE、闭合子目录、父/子写区、模拟重解析点事实 |
| R5 回执混用 | 精确已登记根、预期 run 与 cohort，不是只排除几个旧根 |
| R6 重复 job | 同 cohort 不同 job 允许，同 job 重复/坏占位状态拒绝；不声称持久/原子 native 防重 |
| R7 历史回改 | 独立上一快照 SHA、删除/字段变更/回滚/非法跳转及根 ID 复用拒绝 |
| R8 放宽白名单 | 非空严格子集、重复/绝对/嵌套/通配子目录拒绝 |

mock_root_boundary_checker.py 是纯模型，默认只输出固定夹具结果；--receipt 仅向项目内新文件写回执，拒绝已存在文件/冻结目录/ADS/重解析路径。源码内部 13 个固定场景与 test_mock_root_boundary_checker.py 的 28 项独立对抗回归分别记账，不把场景个数累加为原生证据。新版回执 scope=SYNTHETIC_MODEL_ONLY_NOT_NATIVE_ACCEPTANCE，带实际源码 SHA。

## 6. 后续实施与验收

1. 先审本设计与静态模型，再交统一 per-run 上下文/真实根处理器、可信历史保管、OS 路径与 ACL、持久原子 job 预留及相关对抗候选。
2. collector、transport、full-surface/legacy verifier、外部 driver/inspector、automation pins/cohort、证书 schema 与实际根角色一起审查和重新绑定；不能只改 --work、全局常量或放宽 bound_path。
3. 原始源码/pins 变化按影响复核，保留旧证据合同与默认关闭；新的运行配置/快照不能套旧 SHA，实际 worker 加载版本须确认。
4. 在真正获授权的具名范围由 Claude 执行必要固定探针，Codex 不发射；生成场景代码仍受实际 exec_isolation 门禁。D2/D8 延后 GAP 不阻塞准备。
5. Codex 依据真实父证据、原件/媒体和当前绑定独立复算，再另行裁定资格。Mock 合格不代替 Windows 原生、全 43 点或生产解禁；全局 NOT_ESTABLISHED、production=CLOSED 不变。
