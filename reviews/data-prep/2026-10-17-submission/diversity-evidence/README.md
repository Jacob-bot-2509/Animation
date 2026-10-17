# 多样性绑定准备 v2

Codex 已修复 build_diversity_bindings.py：核验当前manifest中训练文件的 SHA和字节数，拒路径穿越/ADS/重解析、重复文件/ID、缺失或冲突身份、错误JSON和重复键；捕获同一份manifest、policy与数据原字节，前后复查。每条绑定含文件SHA、真实行号、原始行（含结束字节）SHA与规范记录SHA。

当前有效代际：
generation-6896eb72b7f2404caac8f2244e791b75/

该目录包含47条当前train绑定及47条待审记录，政策概念数53；COMPLETE.json最后写入并绑定三个输出文件。原目录中的 row-bindings.jsonl、pending-review-list.jsonl、template.json 保持作者原字节，供历史比对；新的代际是本轮应审版本，不把两套文件合并计数。

生成器仅写本目录下全新 generation-<32位hex> 子目录，独占创建，不覆盖原件。出现写入失败、输入变化或缺COMPLETE的代际均不能视为完整，不能删除占位后自动重跑。目录完整性标记仅证明绑定准备完整，不是审核通过或断电持久/恶意同权进程安全证明。

18项独立测试通过，实际47条来源、原始行、规范记录SHA均另行核对；原作者47个原始行哈希与当前结果一致。所有concept、variant、user_review、数学、多样性、泄漏裁决仍为null/PENDING。不生成 data/training_diversity_evidence.json，不改validate.py，不代填APPROVED。47条绑定不等于53概念政策已经满足。

production=CLOSED。后续真实审核应产生独立且绑定本代际的材料，不把本模板本身当用户意见。

Intermediate generation generation-b61ba8e7d1ff4edc87a9c477b3d6336d is retained with its original builder SHA; use only the current generation above for this delivery.
