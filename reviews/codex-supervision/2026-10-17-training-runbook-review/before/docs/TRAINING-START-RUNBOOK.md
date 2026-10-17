# 训练开工 Runbook(2026-10-17 夜,门禁未开)

> 状态快照来源:本机 preflight 实测(2026-10-17 01:4x)+ configs/hp_sweep.json(用户已确认)
> + docs/TRAINING-LOOP-DESIGN.md。设计契约不变:门禁自检前置,fail-closed,证据链完整。

## 一、当前门禁状态(preflight --manifest data/manifest.json 实测)

PASS:
- gpu:NVIDIA GeForce RTX 5060 Laptop GPU, 8151 MiB
- data_manifest:6 条目,问题 0,quarantine 0
- freeze_gate:冻结证据绑定当前 manifest,eval/test 全量覆盖
  (注:裸跑不带 --manifest 会误报"无 eval/test 条目",正确姿势须带清单绑定)
- render_gate / math_gate:环境诊断 smoke 通过(非资产验收证据)

FAIL ×3(禁止训练/评测,按顺序修复):
1. **near_dup_calibrated**(UNCALIBRATED):B5 考点签名+5-gram 组合规则缺少独立标签与匹配
   校准证据;组合屏报告自报 calibrated 不能替代独立验收——需 Codex 独立验收口径。
2. **asset_evidence**:样本 calc-area-007 缺产物记录(output 对象)(GS2);
   manifest 训练条目 notes 亦标注"资产/校准仍未通过"。
3. **exec_isolation**:data/execution_evidence.json 缺失——生产隔离联合验收未做
   (对应队列中 exec_isolation 裁决项)。

## 二、开工顺序(门禁开后按序执行)

0. **Codex 最终门禁裁定**(production 解锁):含 exec_isolation 联合验收口径 +
   B5 校准独立验收结论。当前等 Codex 对 watch 部署回执(桥 msg 841)的审查。
1. **数据构建**(门禁后第一步):
   - 绑定 current-core 训练清单到 manifest(hp_sweep.json 的 dataset_manifest 现为
     "TBD:训练启动时绑定 current-core 清单,冻结 SHA");
   - seq2048 构建期逐条 tokenize 校验、超长记录拆分(seq_guard 契约);
   - 资产证据补全(calc-area-007 缺产物记录——用已验收交付回填,不造数据);
   - 冻结锁重绑(--check 现全绿,构建后按新清单重冻)。
2. **preflight --ready 全绿**(gpu/model/data_manifest/run_snapshot 无 FAIL 无 UNVERIFIED)。
3. **试训网格**:hp_sweep.py --config configs/hp_sweep.json —— 4 组
   (2 LR × 2 r,pilot 78 条约 1/4 训练数据,seed 20261005),每组约 5-15 分钟;
   按 eval_loss + 生成动画样本双指标选胜,写回 configs/train_loop.winner.json。
4. **全量训练**:train_loop.py 以 harness 后台长跑(分离式隐藏进程,日志落 runs/,
   单进程编排全部轮次;分层目标 R=100% 且 E≥95% 停/连续 3 轮平台停/上限 8 轮;
   runs/loop.stop 可中止)。claude-code 盯每轮报告,异常/完成汇总给用户。
5. **holdout 泄漏检测**:391 条冻结真题,统计置信区间对照 eval 基线(硬门禁,
   过线才进入审片)。
6. **用户审片**:看动画样例 → 自然语言反馈 → claude-code 分诊落地
   (数据问题改 scene_spec/补数据;模型问题调参)→ 回到 3 迭代,点头才放量。

## 三、命令速查

```bash
# 门禁自检
.venv/Scripts/python.exe -X utf8 tools/preflight.py --manifest data/manifest.json \
    --model .models/qwen3-4b --ready --run-id <run_id>
# 冻结锁校验
.venv/Scripts/python.exe -X utf8 tools/freeze_data.py --check data/eval-v2.lock.json \
    --manifest data/manifest.json
# 试训网格
.venv/Scripts/python.exe -X utf8 tools/hp_sweep.py --config configs/hp_sweep.json
# 全量训练循环(rounds 配置由 train_loop.example.json 定案后另建)
.venv/Scripts/python.exe -X utf8 tools/train_loop.py --config configs/<rounds>.json
```

## 四、责任划分

| 环节 | 负责人 |
|---|---|
| 门禁裁定 / B5 校准独立验收 / exec_isolation 联合验收 | Codex |
| 数据构建 / 试训网格 / 全量训练 harness 编排 / holdout 检测 | claude-code |
| 审片裁决 / 硬题队列批处理 | 用户 |

## 五、诚实口径

- render_executor / judge_script 未接线(hp_sweep.json 为 null):试训阶段四指标
  M/F 保持 UNVERIFIED,只以 eval_loss + 生成样本目视选优,不假绿;executor 接线后
  重跑扫参即可。
- 全局语义隔离 NOT_ESTABLISHED(用户 2026-10-09 拍板方案 A):接受现状口径开训,
  holdout 391 条冻结真题作硬门禁,训完先过泄漏检测才进审片;测出泄漏按实测指认
  定向修复对应家族后重训。
- IPv6 D2/D8 延期 GAP 记账,不阻塞训练准备(用户授权)。
