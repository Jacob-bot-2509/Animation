# eval/test 审查夹具(synthetic)

> 仅供测试 tools/eval_test_prep.py 的隔离检查;**synthetic,绝不混入正式数据**。

- train_synthetic.jsonl:合成的 train 样本(仅用于隔离检查的对照)
- eval_leak.jsonl:与 train_synthetic 同 problem(换 id)——check 必须检出精确重叠
- eval_ok.jsonl:独立题目的合成 eval 样本——check 应通过
