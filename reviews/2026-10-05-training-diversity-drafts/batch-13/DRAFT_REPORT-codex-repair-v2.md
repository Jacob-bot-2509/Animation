# batch-13 修复版 v2 变更说明

- 基线:v1 `draft-codex-repair-v1.jsonl`(SHA256 `41e18ecb1f1adbd6bc302405dc0f57e26d09ed124bb001a5058239acb5c85d9a`),由 Codex 交付、哈希绑定,本 v2 未改动 v1
- 变更 1:公式内中文改英文(等价记号,数学内容不变),0 处
- 变更 2:scene_spec.steps 补齐「第N步:」前缀 63 条
- 变更 3:Codex msg_484 两处公式格式修正(c07-01 `4\sin^2 3\theta` 加括号、c52-05 的 G(z) cases 补行分隔),0 处
- 涉及题目:仅前缀类修改
- admitted 与 animation_render_verified 均保持 false;数学字段除等价记号外零改动
