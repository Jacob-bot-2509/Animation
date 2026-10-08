# 三方模型筛选决策记录

- 日期:2026-10-03。任务:problem+solution → scene_spec 结构化 JSON(20 条子类分层样本,输入哈希冻结)。
- **用户拍板:baseline = Qwen3-4B(思考模式 80% 严格解析率、训练峰值 5.33G 无溢出)**。
- 落选模型保留在 .models/ 作后续对照,不删除:
  - Qwen2.5-7B-Instruct(35%,训练 9.4G 溢出)
  - Qwen3-8B(65%,训练 10.12G 溢出)
- 完整证据:MODE_COMPARISON.{md,pdf} 与 evidence/(各 run 逐样本输出/摘要)在本目录;
  临时实验组 outputs/screening-tmp/ 已按 cleanup-manifest 撤走。
- 下一步:回归正式实验主线(eval/test 独立制作与冻结 → preflight 八项门禁 → 训练批准)。
