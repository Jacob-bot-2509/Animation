# 首轮审查报告（历史基线）
日期：2026-09-30。范围：c0b0ed6 至 28d916b，累计审查，未逐提交运行历史测试。
原始结论：BLOCKED。已有 45 项测试通过，合成反例仍暴露以下问题。本文件从本次会话的审查记录重建为 UTF-8；原中文在 PowerShell 管道传输时丢失，旧证据未删除。当前修补进度见 reviews/2026-09-30-sync/REVIEW.md（若尚未生成，表示本轮复审进行中）。

| 编号 | 严重性 | 原始问题与定位 | 修补验收 |
|---|---|---|---|
| R1 | P1 | tools/split_data.py 写出可覆盖 pool；make_manifest/check_fields/run_record 无统一保护，记录先写后验 | 全部输入输出路径检查；默认拒绝覆盖；冻结 eval/test；失败不修改原数据；记录验证后保存 |
| R2 | P1 | split_manifest 与 Manifest.load 不兼容；scan 将平铺 split 文件全标 raw | 标准契约可串联；角色显式登记；来源/许可证继承；输入输出哈希；相对路径正确 |
| R3 | P1 | validate/schema 允许缺 source/SHA、坏 JSON；路径解析后未约束根目录 | schema/类型/哈希/size/provenance 完整；所有阶段只读合法路径；错误明确定位 |
| R4 | P1 | validate 只对 train 比较，漏 eval/test ID 重叠 | 三集合两两 ID/内容/文件 hash 无重叠；近重复完整报告与阈值校准 |
| R5 | P1 | preflight 只查 GPU 就能通过，空 JSON 无权重目录被判齐全 | 诊断与严格模式分开；严格聚合必需 L1–L5 证据；缺项/跳过阻断；模型完整性可验证 |
| R6 | P1 | code_gate 别名调用绕过黑名单 | 原名、import/from-import 别名有反例；静态检查不能替代执行隔离；数学/渲染未验证明确标注 |
| R7 | P2 | fields 把 answer=0 判空；第二行缺字段报 line=1 | 合法零值保留；真实物理行号；按类型验证核心字段 |
| R8 | P1 | run_record 对缺 manifest/env/seed 证据仍通过，不能证明重放 | 完整配置/代码/数据/环境/种子证据，真实文件校验，校验后保存，不覆盖旧记录；L7 固定评测契约 |

初次证据：reviews/2026-09-30-initial/probe_results.json 与 fixtures；仅使用新建合成样例复现覆盖，未执行危险代码字符串。此处 JSON 中原中文说明也可能损坏，但英文键、布尔结果与路径仍可用于核对。

阶段结论：c0b0ed6/R3 阻塞；3fb662a 的 quarantine 非默认通过行为验证通过，但 L1 未完整；c963a4a/R4 阻塞；3a3fd5c/R1/R2 阻塞；e0d435b/R7 阻塞；846da29/R6 阻塞；23ca661/R8 阻塞；8272285/R5 阻塞；28d916b/L7 证据不足。之后修复必须单独注明 HEAD 和测试覆盖，不能把原结论当作当前修复结论。

近重复 0.7 为未校准初值；JSON 原始行相似度和 top20 候选不能证明穷尽无重复。真实 API/数学/渲染未验证。发布前还需补齐忽略规则、更新 README 并由用户确定许可证。
