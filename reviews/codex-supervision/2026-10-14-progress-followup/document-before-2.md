# 环节入口(每个工作环节从哪进)

## 2026-10-13 当前入口：OneDrive材料自动化与训练准备

- [第二三层方案](../../reviews/codex-supervision/2026-10-13-witness-automation-design/DESIGN.md)：用户已选OneDrive；当前交付设计、配置与协议，新工具尚未实现/部署。
- [执行口径](../../reviews/codex-supervision/2026-10-13-witness-automation-design/POLICY.json)：D2/D8仍GAP且延期，不阻塞训练准备；此授权不启动训练或放行生产。
- [配置模板](../../reviews/codex-supervision/2026-10-13-witness-automation-design/config.example.json)：active=false，实际两端同步目录、证人采集根和sender批准绑定待配置。
- Codex负责材料打包/消费与独立审查；探针和采集启动由用户授权后Claude执行。新作业保留完整SHA，不写冻结旧all43根。下方历史入口不能替代当前授权范围和资格。

## 1. 审阅 264 题

- 打开:`reviews/codex-supervision/2026-10-05-harness-strict-fix/pdf-v5/draft-review-harness-v1.pdf`(138 页权威版)
- 每题五块:题目 → 推导 → 答案 → 场景对象 → 场景步骤
- 审四层:数学 / 题干 / 场景可动画性 / 格式风格
- **发现问题只报题号**(如 `batch-07 c16-04`),我走修复链

## 2. 修复链(审出问题后)

1. 按题号定位草稿记录(选中版本:4 批 v6 + 14 批 v4-final)
2. 改题 → 重算哈希 → 用 `tools/publish_row_patches.py` 发布**新版本**(旧的 v5/v6 入口已退役,禁止复演)
3. 重跑审计(draft_audit)与渲染 → 更新审阅 PDF(只出新文件,不覆盖旧版)

## 3. 门禁检查

```powershell
# 数据总校验(manifest/锁/重叠/许可证)
.venv/Scripts/python.exe tools/data_check.py --manifest data/manifest.json

# 训练就绪综合门禁(需 run-id 参数,见 preflight --help)
.venv/Scripts/python.exe tools/preflight.py --help
```

三项门禁现状(看 `data/asset_evidence.json`、preflight 输出、监督报告):
- 结构检测器校准:near_dup_calibrated=false；171对开发诊断即使真实标注也不能自动成为独立校准
- 资产验收:1/497 已验收,门禁 NOT READY
- 生产隔离:exec_isolation 保持 CLOSED(用户裁决:全安全点全绿才解禁)

## 4. 超参确认(等你拍板)

- 文件:`configs/train_loop.example.json`
- 内容:LR "1/5000"、batch 2×4、epochs 6、LoRA r8/α16、seq 2048、4bit、seed 42
- 动作:你确认 → status 设 CONFIRMED + 计算 sha256 绑定(门禁校验该绑定)

## 5. 与 Codex 协作

```powershell
cd D:\code\.bridge-poll
python bridge_poll.py poll          # 读新邮件(读后即已读)
python bridge_poll.py send task_result "内容"   # 回信
```

- 分工按当前交接划定文件所有权,不以工具目录永久归属代替沟通。Codex本轮已交付并释放两段准入工具源码；Claude负责修订场景实际隔离重渲染,248帧修订视频已由Codex局部视觉复验，标准v2回执已独立核验；自动语义验收被拒，仍须完成完整真实语义审阅
- Codex 发来的哈希/报告一律先核验再采信

## 6. 训练入口(门禁全绿后才可用)

- 训练:`tools/train_loop.py`(带门禁检查,超参未 CONFIRMED 会拒绝)
- 基线测速:`tools/bench_throughput.py`(本机 RTX 5060 8GB 实测:LoRA 1.69s/步、生成 10.2 tok/s)

## 7. 剪切题的当前验收入口

- 最新回执/语义复验：[监督报告](../../reviews/codex-supervision/2026-10-06-bound-receipt-semantic-review/SUPERVISION_REPORT.md)；源码/工具修复仍见 `reviews/codex-supervision/2026-10-06-repair-progress-followup/SUPERVISION_REPORT.md`。
- 修订场景：工具修复报告同目录 `shear-scene-v2.py`；02:10–02:11 已实际重渲染，248帧、15帧每秒，原四项画面缺陷已解决。12:07的新标准v2回执已独立核验；旧自定义回执保留为历史。当前自动语义验收被拒，未激活提案不得正式升版。
- 渲染：`tools/admit_linalg048_v3.py --scene <修订场景> --out <项目内新的回执>`，通过后仍待人工视觉/语义验收。
- 语义待审材料：`tools/review_linalg048_pairs.py --render-evidence <标准v2回执> --out <新待审包>`；296唯一题、496完整来源记录，判定留空，不是人工验收。
- 提案：`tools/apply_linalg048_admission.py --render-evidence <绑定v2回执> --acceptance <真实完成的人工审阅> --out <新的提案>`；此工具只出未选择提案，不直接切换五个现役文件。
- 当前开发诊断：工具修复报告同目录 `diagnostic-current-v3/`；旧150/171对文件保留为历史，部分旧来源绑定已过时。
- 资产来源新进度：工具修复报告同目录 `assets-progress-rebound-v4.json`，仅修正15条文件SHA，保留1/497已验收与NOT READY；尚未选择发布，不代表剪切素材验收通过。
