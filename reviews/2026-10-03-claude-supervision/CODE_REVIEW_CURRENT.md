# 当前代码与 Claude Code 邮件复查（2026-10-03）

审核基线：HEAD 4fe0152，以及当前未提交工作树。最新收到 Claude Code 邮件 msg_263（北京时间 22:10:14），报告 v2 候选生成完成，正式引用切换仍待批准。

完整测试：360 passed + 29 subtests passed。代码 diff --check 通过。测试全绿不能替代以下具体反例。

## 待整改问题

| 优先级 | 位置 | 问题与实测影响 |
|---|---|---|
| P1 | src/animtrain/render_gate.py:244、src/animtrain/preflight.py:159 | 网络隔离仍无条件标 True，执行门禁报 PASS。先前回环实验已证普通 socket 被拦但底层 _socket 可连接；相关实现未变。应区分常规调用保护与有效隔离边界。trusted=False 仍拒绝不可信代码，此保护保持有效。 |
| P1 | tools/preflight.py:139 | 把 data/ 下所有版本锁均要求绑定当前清单。v2 两锁分别绑定合法 v2 子清单，却被拿来与当前 v1 主清单比较，导致已验证的 v1 freeze_gate 失败。当前 CLI 已重现。 |
| P1 | tools/make_eval_test.py:204 | v1 保护只比较大小写敏感的路径片段。Windows --out data/V1 绕过，代码将写入同一个 v1/eval/dataset_eval.json。用截获写入安全探针证明，未实际改生产文件。应解析实际目标、比较同一文件/目录并应用冻结保护。 |
| P2 | tools/eval_test_prep.py:46 | --dir data/v2 仍绑定 ROOT/data/v1/manifest.json，并混入 v1 锁。v2 锁自身验证通过，却被 status 报为不覆盖/绑定不一致。应按选定版本和数据集合选清单及锁。 |
| P2 | src/animtrain/metrics.py:62、106 | 未提交指标补丁不验证 parsed_strict/parsed_lenient 的布尔类型。传 2/2 被视为成功，严格和宽松解析率都输出 2，即 200%。应拒绝非法标志，保证率值范围。 |
| P1（内容） | dataset-eval.md:982、data/v2/eval/dataset_eval.jsonl:69 | 新自包含解答仍称两形式“均为完整实不可约分解”。形式二含 x^4+1，可继续分解为 (x²−√2x+1)(x²+√2x+1)，因此该结论错误；这条独立解答也没给出题面要求的复数域分解。场景字符串互异不证明数学正确。 |

## 已独立确认

- v2 审计 CLI 已支持 --base data/v2，本次明确检查的是 v2。结构/身份/镜像检查未报 hard；450 条仍 quarantine，主要缺真实动画验收证据与许可证限制等。
- v2 两份子清单各 1 条 JSONL，data_check 通过；两份锁配各自 v2 子清单校验通过。
- train/eval/test 精确交叉重叠 0，当前阈值下近重复越界对 0，阈值仍 UNCALIBRATED。
- v1 两份 JSONL、主清单和两把锁与 d701ee4 字节一致，没有被 v2 提交覆盖。
- 抽查原反例，积分/裂项/凝聚以及生成函数的方法内容已区别；本次没有做 300 条数学内容的完整逐条验收。

## 工作树与范围

当前源码改动主要是未提交的 metrics.py 及相关测试；新增提交改动 make_eval_test.py 与 v2 数据。pyproject.toml 还存在 0.2.0→0.1.0 的未提交回退，发布文档删除及旧审计证据变动也不属于 v2 提交，应确认归属后再纳入提交，不能无差别打包。

本轮仅检查与留档，没有修改源码、冻结数据或正式引用，没有启动训练。

证据：evidence/pytest-current.log、preflight-current.log、audit-current-v2/、generator-v1-alias-probe.json、metrics-nonboolean-probe.json，以及先前 network-loopback-bypass.json。已通过 msg_264 向 Claude Code 发回反例。
