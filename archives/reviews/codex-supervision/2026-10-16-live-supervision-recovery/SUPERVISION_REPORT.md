# Claude 当前工作与只读监听修复

截至 2026-10-16 23:34（UTC+8），当前可核实的新进展是 OneDrive 接入准备：local 配置仅将 consumer.sync_root 从 null 改为 C:\Users\Jacap\OneDrive\witness；active=false，证人 capture_root、sync_root 仍为 null。四工具源码未变，未发现新的跨端同步回执或证据 job。不能仅凭文件时间确定编辑者，也不能把已填目录当作共享权限或同步已验收。

Claude 最近一封实质回执为 msg_1792162910315_830，确认按 Codex 修复版本推进并等待材料。邮箱无待审批次；桥注册最后活跃时间、进程存在或采样子进程为空均不证明某任务正在执行、已完成或卡死。

## 本次由 Codex 修复

发现监督链本身存在三个问题：

1. 只读观察器最新心跳停在 2026-10-14T01:44:25.818452+08:00，原 worker 已不在。末条事件为 CIM 失败，实际退出原因未知。
2. 归档后 reviews/codex-supervision/latest-live-file-hashes.json 入口缺失，会阻止旧观察器重新启动。已从 archives 下同名原件恢复完全相同字节，SHA256 db1c3c46bb93b8a26f622f9c86727ba0b9a3b0c9ee94bd9c82eb84644c5a07bd；没有重新设定历史基线。
3. 原进程查询异常会跳过整轮文件/HEAD 心跳。已修改 watch_claude.py：进程查询显式返回 OK/UNAVAILABLE；查询失败时文件采样继续；不把失败当作空进程树，不报告虚假的进程退出；恢复后先建立进程基线。

具体文件：
- reviews/codex-supervision/2026-10-04-live-watch/watch_claude.py：容错修复，加入四工具、配置及独立新 job 回执监听；不扫描 OneDrive 根，忽略 job ZIP/partial 重复内容扫描。
- tests/test_live_observer_recovery.py：12 项针对性回归；临时夹具位于可写的 reviews/witness-automation/test-work，避免重跑写入冻结归档。
- reviews/codex-supervision/latest-live-file-hashes.json：恢复原字节兼容入口。
- reviews/codex-supervision/2026-10-04-live-watch/README.md：更新实际恢复情况与边界。

旧日志和冻结目录未修改；活动状态/事件正常更新，并另记观察空窗，不补造历史采样。保留其他工作者对 local 配置的修改；不重复改 .gitignore 或自动化工具。未提交 Git、未改邮箱调度源码或计划任务、未启动采集/探针/OneDrive consumer worker。

## 独立验证与当前实际运行

最终测试版本 12 项通过，另有 verification.json 中 26 项具名版本/状态检查通过；两组数量不混作测试用例总数。覆盖 CIM 错误、超时、非法快照、重复 PID、失败时文件心跳继续、跨失败空窗不虚构进程变化、恢复基线及回执扫描。首次测试后仅把测试夹具改到可写命名空间，再验证最终版本；既有 28 项证据工具回归未重复跑。

已隐藏恢复只读观察器：launcher 48632，实际 worker 51704。至少两次真实心跳分别为 23:31:22.366683 与 23:32:19.271627，末次核验样本为 23:34:08.142925，进程查询 OK。真实尝试启动第二实例被 Watcher already running 拒绝，原实例继续采样，stderr 为空。

采样看到 Claude PID 47296、conhost 子进程，无其他子作业；这里只说明采样时点结果。后台仅记录变动，不进行模型审查或自动批准。后续完整审查仍依赖本会话/邮件实际处理。

原四项 core_drift 与恢复前完全相同：
src/animtrain/network_isolation.py、src/animtrain/appcontainer.py、src/animtrain/render_gate.py、reviews/2026-10-04-acceptance-support/network_acceptance.py。
保留相对历史基线的偏离，不把重启等同于修复这些差异或准入通过。

## 版本与交接

watch_claude.py SHA256：
bd29b8548f1f9318c0ebb537d68f12862f65180027b52504c7a8edbf4ca484d4。

新测试 SHA256：
908c4e75de4a183df2e97fbe06c7599a4c1e74cfdc46d1134dd01786d10cc8d3。

当前 local 配置 SHA256：
57425199bd77aa8380323563bdd92d8d70499297bd7a47a350041d6ccc3f5e6c。

当前 HEAD：
e8a0aa88ef750aaaa3e8b9f3e0cee1985b11c5cc。
工作区已有路径迁移、三个导航文档和 .gitignore 改动，经对应归档绑定核对予以保留；没有把这些既有 Codex 改动误作 Claude 新错误。

修复后合格范围：本机只读观察器的进程查询容错、文件/HEAD 心跳、单实例与具名监听恢复。实际 OneDrive 通道仍 NEEDS_EVIDENCE。下一步由 Claude 汇总证人两个路径、两端专用共享权限/可达情况、证人 Python 与工具布局，再提交真实跨端包与消费回执。已填训练机路径仍需按实际接入证据核验，不能以配置值代替授权/权限和可达性事实。

D2/D8 保持延期 GAP、不阻塞训练准备；D1/D7 依赖不变。全局隔离 NOT_ESTABLISHED、原生沙箱 UNVERIFIED、production=CLOSED。本次不重签数学或视觉资格。

完整原始 stdout/stderr、前后源码、配置快照、心跳、单实例拒绝、空窗记录和版本检查均在本目录。Codex 将实际回信说明已修改内容与合格范围，要求 Claude 按修复版本继续后续工作，不重复修改已完成部分；真实回执在封存时纳入 delivery-manifest.json。
