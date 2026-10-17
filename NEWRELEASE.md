# Animation Model Training v0.6.0

发布日期：2026-10-17
发布类型：通道验证与门禁前准备收口版（Pre-release）

本版本同步 10-13 至 10-17 的进展：OneDrive 证据通道端到端验证通过并转为常驻服务、门禁前静态准备全套交付且全部获得 Codex 独立裁定、首批 10 题完成精确数学复核与渲染试点、呈现管线 harness 上线、训练数据全量备份。生产门禁保持 CLOSED，训练未启动。

## 版本可重现性

本版本提交 99d27855 起（含更早 3eeed869、a6046174、d2b7b3b3、953f7927、0fcfe010 等本周期提交）。审查链归档于 archives/reviews/codex-supervision/ 与 archives/harness/、archives/codex/（2026-10-17 用户指示分档）；在审材料在 reviews/data-prep/2026-10-17-submission/。自动监管活体文件（worker.lock/state.json/latest.json）不入库。

## 本次交付

### 证据通道与常驻服务（本轮核心）

- **OneDrive 通道端到端验证**：WJW 证人机 pack（LOCAL_PUBLISHED，包 SHA 7d25d860… 与回放字节一致）→ 跨端 OneDrive 同步 → 训练机 consumer 对账 REGISTERED_RECONCILIATION_COMPLETE → WJW 实跑配置与回执回传归档。Codex 独立裁决 **PASS_BOUND_ONEDRIVE_REPLAY_CHANNEL**（89 项材料核验）。
- **watch 常驻部署**：Codex 修复 consumer 生命周期锁（全生命周期单实例），部署验收 **PASS_CURRENT_BOUND_CONSUMER_WATCH_LOCAL_DEPLOYMENT**（46 项核验；首扫幂等、第二实例拒绝、STOP 退出码 0 实测）。部署记录在 reviews/witness-automation/runtime/deploy-records/。
- 实验传输件按用户指示清理（10 项，归档副本保留）；服务中断后由 Codex 按原验收版本恢复（退出原因 UNKNOWN 如实保留）。

### 门禁前静态准备（全部获 Codex 裁定）

- **数据策略定稿**（用户拍板）：NuminaMath 抽样上限 2000（首批 300）；TheoremQA 800 + UGMathBench 5062×3 为 EXTERNAL_QA_ONLY 外测（GPL-3.0 不进训练）；manim 类四集许可未标仅作风格研读；用户审核带宽=全量目视。
- **来源登记与抽样设计**：三来源固定 revision 登记 + 六层配额方案 + 7 学科×3 难度整数配额（300）+ 整数最大流可行性核验器（17 回归）；execution_ready=false，未下载未抽样。
- **评测接线夹具**：eval-wiring 协议 harness，20 自动断言 + 18 对抗回归 + 15 绑定检查全过；正式 R/E/M/F 全 UNVERIFIED，诊断单列 fixture_diagnostics。
- **执行器/判定器合同**：设计 v2（四组件边界、受限数学 DSL、F 清单帧定位、接线序列）。
- **exec_isolation 准备**：BOUND_FILES 清单（15 绑定文件 + 3 采集脚本当前 SHA）+ 新根方案（版本化注册表 + cohort + 拒绝矩阵，REPAIRED_PASS_DESIGN_AND_PURE_MOCK_ONLY）+ 根处理器静态实现（39 项 unittest）。当前 43 点面：30 GREEN / 2 PARTIAL（F2/F4）/ 11 GAP；execution_evidence.json 缺失，联合验收 NEEDS_EVIDENCE。
- **资产证据根因**：496/497 未过的共同根因定位为 tools/render_templates.py 的 step[:28] 硬截断 + steps[:5] 限步 + Text 吞公式 + 答案无兜底；模板修复候选 v3/v4（分页覆盖证明、混排显式失败、精确分数白名单）+ 首批 10 条多故障覆盖清单 + 内容/几何映射 + 数学对应材料。
- **diversity 准备**：47 条 train 原始行 SHA 绑定表（含行结束字节，交叉验证一致）+ 结构模板 + 待审清单（审核字段全 null，不代签）。

### 首批 10 题精确数学复核与呈现管线（Codex 独立完成数学复核）

- Codex 完成 10 题逐题精确数学复核：35 项手写表达式核验通过，9 处实质修订（birthday 精确式、LLN/CLT 条件补正、半开矩形边界、单位圆夹逼、Green 规格绑定、p 级数下界、M-test 尾项、旋转体体积推导等），裁定 REPAIRED_PASS_EXACT_MATH_TEXT_CANDIDATES_ONLY。
- **呈现管线 harness**（v2，Codex 修复版）：generate（独立重算校验）/ render（check_certificate 权威门禁，恒 rendered=false 直至 exec 证据）/ review-pack（原子重建 10 包 + 三选一结论单）/ --verify（机器可验签名两态）。40 项测试全过。
- **渲染试点**：10 题文字候选在 AppContainer 内渲染成功（45 帧 MP4 + 联系表；0 几何图元，network_isolated=false 如实记录）——证明文字层可渲染，不构成 exec 验收。
- **几何层设计**（DESIGN，待审）：10 题 → 10 类几何模板映射 + 每模板 F 取证合同（fidelity-checklist 逐项帧定位）。

### 数据备份与工程

- **训练数据全量备份**：data + holdout-sources（391 冻结真题池）+ configs + archives + reviews/data-prep 共 113,594 文件 / 7.04GB，逐文件 SHA 清单；robocopy 逐目录 rc 保留。
- 归档分档：archives/harness（harness 报告与修正记录）+ archives/codex（Codex 报告新约定）。
- IPv6（D2/D8）：新轮要求已交付（PASS_PLAN_ONLY，NEW_ROUND_REQUIREMENTS.md），用户决定先不做，GAP 记账不阻塞。

## 状态与边界

- production=CLOSED、execution_evidence.json 不存在、全局隔离 NOT_ESTABLISHED、原生沙箱 UNVERIFIED。
- 渲染试点与夹具均不构成 43 点证书；正式渲染须 check_certificate + 获准入口。
- 训练未启动；试训、holdout、审片、全量训练均待门禁解锁与直接授权。
- 本版本不是训练完成或生产就绪版本。

## 下一步

1. 几何层设计审定 → 逐模板实现 → 首批 10 题图解渲染与 F 取证。
2. exec_isolation：新根接线许可 → 用户授权补采 → Codex 独立复算 → 43 点收口。
3. 资产 496 条批量重生成/重渲染/双重审核（用户全量目视分批）。
4. B5 独立标签材料、diversity 47 条真实审核、NuminaMath 抽样执行。
5. 全部收口后 Codex 最终门禁 → 数据构建 → 试训网格 → holdout → 审片 → 全量训练。
