# 项目备份只读核验候选

工具 verify_training_backup.py 只读取项目及已观察的备份 D:/backups/animtrain/2026-10-17-training-data。只在本目录新建 audit-UUID 报告，不执行复制、覆盖、删除、同步或还原，不读取题文作额外数学/历史审查。

默认模式核验 data、holdout-sources、configs 全树，按路径集合、目录集合、字节数和SHA比较，并检查读取前后可见的元数据变化、重解析点和共享文件身份。资源上限为每树30000文件及4GiB字节预算，另检查两树合计预算；超限或错误返回2，不能判为通过。该预算不是完整项目大小的承诺。

当前范围模式：项目venv的Python -X utf8 -B verify_training_backup.py --current-inputs-only。
只核验当前 data/manifest.json 的六个数据文件，以及 data/manifest.json、data/asset_evidence.json、configs/training_diversity_policy.json、configs/train_loop.example.json 四个控制文件。核清单SHA/大小、源与副本SHA、读取前后可见变化。该模式成功只表示具名输入一致，整个备份、holdout-sources及其他配置仍未审计。

本轮最终报告：audit-bf0888beb0f24d7f97e6fcc9a5b0a559/。10文件、1283186字节一致。原完整树尝试 audit-b64313357f1d4e77a95fb78be29927c0/ 因资源上限返回ERROR，不能删除它来宣称全量通过。较早的 audit-6d4f851cd38a48d3a1049edfe9011d8d/ 是加清单大小校验前的中间结果，最终结论引用具名最终版本。

21项独立回归与独立 file_digest 实际复算见归档：
archives/reviews/codex-supervision/2026-10-17-backup-integrity-review/FIX_REPORT.md

后续复制步骤的质量要求：在原有实际授权范围内，逐子目录保留真实命令、起止时间、源/目标、robocopy退出码和stdout/stderr；按工具合同解释每个退出码，不能仅凭PowerShell整体成功或文件数报告完成。目标使用具名新版本，避免混入旧文件；核验发现多余/缺失/错配只报告，不自动删除或覆盖。本工具可独立补足当前文件内容检查，但不能补写历史退出码，也未自动接入原复制命令。

范围限制：同盘字节一致不等于异机/异盘容灾、ACL/密钥/访问隔离、还原演练或原子快照；不保证恶意并发写者无法保持元数据。当前候选数学修订位于archives，不在此次备份三个目录内，不能把本结论称为整个项目或修订成果已备份。production=CLOSED、全局NOT_ESTABLISHED；不启动训练。
